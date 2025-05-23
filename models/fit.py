import sqlalchemy
from sqlalchemy import text
import rdflib
from rdflib import Graph, URIRef, Literal, RDF
from rdflib.namespace import RDFS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# تعريف الكلاسات
class Cardio:
    def __init__(self, stage, body, sex, sessions, time):
        self.stage = stage
        self.body = body
        self.sex = sex
        self.sessions = sessions
        self.time = time


class Gym:
    def __init__(self, day, exercise, sets, reps):
        self.day = day
        self.exercise = exercise
        self.sets = sets
        self.reps = reps


class Exercise:
    def __init__(self, id, name, link, overview, introductions):
        self.id = id
        self.name = name
        self.link = link
        self.overview = overview
        self.introductions = introductions

    def get_overview_paragraph(self):
        return self.overview.split(';')

    def get_introductions_detail(self):
        return self.introductions.split(';')


# الاتصال بقاعدة البيانات
def get_all_exercises():
    engine = sqlalchemy.create_engine("sqlite:///E:/Knowledge Project/eat-and-fit.streamlit-master/eat-and-fit.streamlit-master/database/eatandfit.db")  # تعديل المسار الصحيح لقاعدة البيانات
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Exercise")).fetchall()

        # تحويل كل صف إلى كائن من كلاس Exercise
        exercises = [Exercise(*row) for row in result]
    return exercises


# إنشاء RDF Graph وتوليد البيانات الدلالية
def create_rdf_graph(exercises):
    g = Graph()

    # إنشاء مساحة أسماء لـ RDF
    exercise_ns = URIRef("http://example.org/exercise/")
    g.bind("exercise", exercise_ns)

    for exercise in exercises:
        exercise_uri = URIRef(f"{exercise_ns}{exercise.id}")
        g.add((exercise_uri, RDF.type, URIRef("http://example.org/Exercise")))
        g.add((exercise_uri, RDFS.label, Literal(exercise.name)))
        g.add((exercise_uri, URIRef("http://example.org/overview"), Literal(exercise.overview)))
        g.add((exercise_uri, URIRef("http://example.org/introductions"), Literal(exercise.introductions)))

    return g


# استعلام SPARQL للحصول على تمارين معينة
def query_exercises_rdf(g):
    query = """
    PREFIX ex: <http://example.org/exercise/>
    SELECT ?name ?overview ?introductions
    WHERE {
        ?exercise rdf:type ex:Exercise .
        ?exercise rdfs:label ?name .
        ?exercise ex:overview ?overview .
        ?exercise ex:introductions ?introductions .
    }
    """
    return g.query(query)


# توليد PDF تقرير مع التفاصيل
def generate_pdf(exercises):
    c = canvas.Canvas("exercises_report.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, "Exercises Report")
    y_position = 730

    for exercise in exercises:
        c.drawString(100, y_position, f"ID: {exercise.id}, Name: {exercise.name}")
        y_position -= 20

        # إضافة تفاصيل الـ overview و introductions
        overview = exercise.get_overview_paragraph()
        introductions = exercise.get_introductions_detail()

        # إضافة التفاصيل في التقرير
        c.drawString(100, y_position, f"Overview: {'; '.join(overview)}")
        y_position -= 20

        c.drawString(100, y_position, f"Introductions: {'; '.join(introductions)}")
        y_position -= 20

        if y_position < 100:  # إذا كانت الصفحة ممتلئة
            c.showPage()  # إضافة صفحة جديدة
            c.setFont("Helvetica", 12)
            y_position = 750

    c.save()


# تنفيذ الوظيفة وجلب كل التمارين
if __name__ == "__main__":
    exercises = get_all_exercises()

    # إنشاء RDF Graph وتوليد البيانات الدلالية
    g = create_rdf_graph(exercises)

    # تنفيذ استعلام SPARQL
    results = query_exercises_rdf(g)

    # طباعة نتائج الاستعلام
    for row in results:
        print(f"Name: {row['name']}, Overview: {row['overview']}, Introductions: {row['introductions']}")

    # توليد تقرير PDF
    generate_pdf(exercises)
