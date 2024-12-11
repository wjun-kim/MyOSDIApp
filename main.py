import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image

DB_NAME = 'scores.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (name TEXT, age INTEGER, gender TEXT, date TEXT, score REAL)''')
    conn.commit()
    conn.close()

def save_score(name, age, gender, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (name, age, gender, date, score) VALUES (?,?,?,?,?)", 
              (name, age, gender, now, score))
    conn.commit()
    c.execute("SELECT rowid FROM history ORDER BY date ASC")
    rows = c.fetchall()
    if len(rows) > 5:
        oldest_id = rows[0][0]
        c.execute("DELETE FROM history WHERE rowid=?", (oldest_id,))
        conn.commit()
    conn.close()

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        if os.path.exists('eyes.png'):
            img = Image(source='eyes.png', size_hint=(1,0.5))
        else:
            img = Label(text="(Eyes Image)", size_hint=(1,0.5))
        layout.add_widget(img)

        title_label = Label(text="건성안 자가진단", font_size='24sp')
        layout.add_widget(title_label)
        
        start_btn = Button(text="Start", size_hint=(1,0.2))
        start_btn.bind(on_press=self.go_next)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def go_next(self, instance):
        self.manager.current = 'userinfo'

class UserInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(UserInfoScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.name_input = TextInput(hint_text="이름", multiline=False)
        self.age_input = TextInput(hint_text="나이", multiline=False, input_filter='int')

        self.gender_male = CheckBox(group='gender')
        self.gender_female = CheckBox(group='gender')
        
        main_layout.add_widget(Label(text="이름:"))
        main_layout.add_widget(self.name_input)
        main_layout.add_widget(Label(text="나이:"))
        main_layout.add_widget(self.age_input)

        gen_layout = BoxLayout(orientation='horizontal', spacing=10)
        gen_layout.add_widget(Label(text="성별(M/W):"))
        gen_layout.add_widget(Label(text="M"))
        gen_layout.add_widget(self.gender_male)
        gen_layout.add_widget(Label(text="W"))
        gen_layout.add_widget(self.gender_female)
        
        main_layout.add_widget(gen_layout)

        next_btn = Button(text="Next", size_hint=(1,0.2))
        next_btn.bind(on_press=self.go_next)
        main_layout.add_widget(next_btn)
        self.add_widget(main_layout)

    def go_next(self, instance):
        app = App.get_running_app()
        user_name = self.name_input.text.strip()
        user_age = self.age_input.text.strip()
        try:
            user_age = int(user_age)
        except:
            user_age = 0
        if self.gender_male.active:
            user_gender = 'M'
        elif self.gender_female.active:
            user_gender = 'W'
        else:
            user_gender = 'N'
        
        app.user_name = user_name
        app.user_age = user_age
        app.user_gender = user_gender
        
        self.manager.current = 'guide'

class GuideScreen(Screen):
    def __init__(self, **kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        guide_text = """
이 설문은 지난 한 주 동안의 안구 건조 관련 증상과 불편함에 대해 묻습니다.
문항별로 해당 빈도를 체크해 주세요.
설문 완료 후 OSDI 점수를 통해 건성안 정도를 확인할 수 있으며,
추가 정보 제공 사이트로 이동할 수 있습니다.
        """.strip()
        layout.add_widget(Label(text=guide_text))
        
        next_btn = Button(text="Next", size_hint=(1,0.2))
        next_btn.bind(on_press=self.go_next)
        layout.add_widget(next_btn)
        self.add_widget(layout)

    def go_next(self, instance):
        # 첫 번째 질문 화면으로 이동 (question_0)
        self.manager.current = 'question_0'

class QuestionScreen(Screen):
    def __init__(self, question_idx, question_text, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)
        self.question_idx = question_idx
        self.question_text = question_text

        self.options = [
            ("한 번도 없음(None of the time)",0),
            ("가끔 있음(Some of the time)",1),
            ("보통 그러함(Half of the time)",2),
            ("자주 그러함(Most of the time)",3),
            ("매번 그러함(All of the time)",4),
            ("해당사항 없음(Not experienced)",0)
        ]
        
        self.selected_value = None
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        main_layout.add_widget(Label(text=self.question_text, font_size='18sp'))
        
        for opt_text, val in self.options:
            hb = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            cb = CheckBox(group=f'q{self.question_idx}')
            cb.bind(on_release=lambda cb, v=val: self.set_selected(v))
            hb.add_widget(cb)
            hb.add_widget(Label(text=opt_text))
            main_layout.add_widget(hb)

        next_btn = Button(text="Next", size_hint=(1,0.2))
        next_btn.bind(on_press=self.go_next)
        main_layout.add_widget(next_btn)
        self.add_widget(main_layout)

    def set_selected(self, val):
        self.selected_value = val

    def go_next(self, instance):
        app = App.get_running_app()
        score = self.selected_value if self.selected_value is not None else 0
        app.scores[self.question_idx] = score
        
        # 문항 진행 상황에 따라 다음 화면 결정
        # 인덱스:
        # 0~4: 첫 5문항(Ocular symptoms), 끝나면 Vision 안내화면
        # 5~8: 다음 4문항(Vision-related-function), 끝나면 Env 안내화면
        # 9~11: 마지막 3문항(Environmental triggers), 끝나면 결과 화면

        # 현재 question_idx 완료 후 이동
        if self.question_idx == 4:
            # 5문항 완료 후 Vision 안내로 이동
            self.manager.current = 'vision_instructions'
        elif self.question_idx == 8:
            # 다음 4문항 완료 후 Env 안내로 이동
            self.manager.current = 'env_instructions'
        elif self.question_idx == 11:
            # 모든 문항 완료 후 결과 화면 이동
            self.manager.current = 'result'
        else:
            # 다음 문항
            self.manager.current = f'question_{self.question_idx+1}'

class VisionInstructionScreen(Screen):
    def __init__(self, **kwargs):
        super(VisionInstructionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        # Vision-related-function 안내 문구
        guide_text = """
시력 관련 기능(Vision-related-function)

지난 주 동안, 눈에 문제가 있어서 다음의 작업을 수행하는 데
제한(혹은 불편함)이 있었던 적이 있나요?

만약 한 주간 다음의 상황을 경험한 적 없다면
"해당사항 없음"을 택하시면 됩니다.
        """.strip()
        layout.add_widget(Label(text=guide_text))
        
        next_btn = Button(text="Next", size_hint=(1,0.2))
        next_btn.bind(on_press=self.go_next)
        layout.add_widget(next_btn)
        self.add_widget(layout)

    def go_next(self, instance):
        # Vision 안내 읽은 후 다음 문항(인덱스 5)으로 이동
        self.manager.current = 'question_5'

class EnvInstructionScreen(Screen):
    def __init__(self, **kwargs):
        super(EnvInstructionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        # Environmental triggers 안내 문구
        guide_text = """
환경적 요인(Environmental triggers)

지난 한 주간, 다음과 같은 상황에서 눈이 불편하다고 느낀 적이 있나요?
만약 한 주간 다음 상황을 경험한 적 없다면
"해당사항 없음"을 택하시면 됩니다.
        """.strip()
        layout.add_widget(Label(text=guide_text))
        
        next_btn = Button(text="Next", size_hint=(1,0.2))
        next_btn.bind(on_press=self.go_next)
        layout.add_widget(next_btn)
        self.add_widget(layout)

    def go_next(self, instance):
        # Env 안내 읽은 후 다음 문항(인덱스 9)으로 이동
        self.manager.current = 'question_9'

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.result_label = Label(text="")
        self.layout.add_widget(self.result_label)
        
        self.link_label = Label(text="자세한 정보: http://www.example.com", color=(0,0,1,1))
        self.layout.add_widget(self.link_label)
        
        end_btn = Button(text="End")
        end_btn.bind(on_press=self.end_survey)
        self.layout.add_widget(end_btn)
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        number_of_questions = len(app.questions)
        sum_scores = sum(app.scores)
        if number_of_questions > 0:
            osdi_score = (sum_scores * 25.0) / number_of_questions
        else:
            osdi_score = 0

        if osdi_score <= 12:
            status = "정상 또는 매우 경미한 건성안"
        elif osdi_score <= 22:
            status = "경증 건성안"
        elif osdi_score <= 32:
            status = "중등도 건성안"
        else:
            status = "중증 건성안"

        self.result_label.text = f"OSDI 점수: {osdi_score:.2f}\n당신의 눈 상태: {status}"

    def end_survey(self, instance):
        app = App.get_running_app()
        number_of_questions = len(app.questions)
        sum_scores = sum(app.scores)
        osdi_score = (sum_scores * 25.0) / number_of_questions if number_of_questions else 0
        save_score(app.user_name, app.user_age, app.user_gender, osdi_score)
        
        self.manager.current = 'start'

class MyOSDIApp(App):
    def build(self):
        init_db()
        self.user_name = ""
        self.user_age = 0
        self.user_gender = "M"

        # 총 12문항: 5(눈의 증상) + 4(시력 관련) + 3(환경적 요인)
        self.questions = [
            # 눈의 증상 관련 5문항 (0~4)
            "지난 주 동안 다음과 같은 눈 증상을 겪으셨나요? (예: 눈의 건조감)",
            "눈이 화끈거리거나 자극감이 있나요?",
            "눈에 모래알 낀 듯한 이물감이 있나요?",
            "시야가 흐릿해지는 증상이 있었나요?",
            "눈이 피로한 느낌이 있었나요?",
            
            # 시력 관련 기능 4문항 (5~8)
            "독서 시 눈의 불편함 정도는?",
            "TV 시청 시 눈의 불편함 정도는?",
            "컴퓨터 작업 시 눈의 불편함 정도는?",
            "야외에서 사물을 볼 때 불편함 정도는?",
            
            # 환경적 요인 3문항 (9~11)
            "바람이 부는 환경에서 눈 불편함 정도는?",
            "건조한 실내(에어컨, 난방기 아래)에서 눈 불편함 정도는?",
            "먼지가 많은 환경에서 눈 불편함 정도는?"
        ]

        self.scores = [0]*len(self.questions)
        
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(UserInfoScreen(name='userinfo'))
        sm.add_widget(GuideScreen(name='guide'))

        # 질문 스크린 생성
        for i, q in enumerate(self.questions):
            scr = QuestionScreen(question_idx=i, question_text=q, name=f'question_{i}')
            sm.add_widget(scr)

        # Vision 안내 화면
        sm.add_widget(VisionInstructionScreen(name='vision_instructions'))
        # Env 안내 화면
        sm.add_widget(EnvInstructionScreen(name='env_instructions'))

        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    MyOSDIApp().run()
