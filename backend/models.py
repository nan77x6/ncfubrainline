from pydantic import BaseModel
from typing import List, Optional


# ---------- User ----------
class UserCreate(BaseModel):
    full_name: str
    role: str

class UserUpdate(BaseModel):
    login: str
    password: str
    full_name: str
    role: str


# ---------- User in Class ----------
class UserClassCreate(BaseModel):
    user_id: int
    class_id: int

class UserClassUpdate(BaseModel):
    user_id: int
    class_id: int


# ---------- User in Subject ----------
class UserSubjectCreate(BaseModel):
    user_id: int
    subject_id: int


# ---------- Class ----------
class ClassCreate(BaseModel):
    class_name: str

class ClassUpdate(BaseModel):
    class_name: str


# ---------- Subject ----------
class SubjectCreate(BaseModel):
    subject_name: str

class SubjectUpdate(BaseModel):
    subject_name: str


# ---------- Themes ----------
class ThemeCreate(BaseModel):
    theme_name: str
    subject_id: int

class ThemeUpdate(BaseModel):
    theme_name: str
    subject_id: int


# ---------- Materials ----------
class MaterialCreate(BaseModel):
    title: str
    markdown_content: str
    theme_id: int

class MaterialUpdate(BaseModel):
    title: str
    markdown_content: str
    theme_id: int


# ---------- Тесты ----------
class TestCreate(BaseModel):
    material_id: int
    title: str

class TestQuestionCreate(BaseModel):
    test_id: int
    question_text: str
    question_type: str  # single, multiple, match

class TestOptionCreate(BaseModel):
    question_id: int
    option_text: str
    is_correct: bool

class TestPairCreate(BaseModel):
    question_id: int
    left_text: str
    right_text: str

class QuestionOption(BaseModel):
    text: str
    correct: Optional[bool] = False

class QuestionPair(BaseModel):
    left: str
    right: str

class QuestionCreate(BaseModel):
    text: str
    type: str
    options: Optional[List[QuestionOption]] = []
    pairs: Optional[List[QuestionPair]] = []
    correct: Optional[int] = None

class FullTestCreate(BaseModel):
    material_id: int
    title: str
    questions: List[QuestionCreate]

class TestTitleUpdate(BaseModel):
    title: str

class TestResultCreate(BaseModel):
    test_id: int
    correct_answers: int
    total_questions: int
    percent: float
