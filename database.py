from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func

# تعريف قاعدة البيانات الأساسية للنماذج
Base = declarative_base()

# تعريف نموذج المستخدم
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    profile_picture = Column(String(255))
    created_at = Column(DateTime, default=func.now())

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")

# تعريف نموذج المنشور
class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

# تعريف نموذج التعليق
class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

# تعريف نموذج الإعجاب
class Like(Base):
    __tablename__ = 'likes'
    like_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")
# معلومات الاتصال بقاعدة البيانات MySQL
# يرجى تعديل هذه القيم بمعلومات الاتصال الخاصة بقاعدة بيانات MySQL التي تستخدمها.
#
# اسم_المستخدم: أدخل اسم المستخدم الخاص بك للاتصال بقاعدة البيانات (في حالتك: root).
# كلمة_المرور: أدخل كلمة المرور الخاصة بك للاتصال بقاعدة البيانات (في حالتك: لا توجد كلمة مرور، لذا اتركها فارغة).
# المضيف: أدخل عنوان المضيف الخاص بخادم MySQL (في حالتك: localhost).
# اسم_قاعدة_البيانات: أدخل اسم قاعدة البيانات التي قمت بإنشائها لتطبيقك (مثال: social_app).
#
DATABASE_URL = "mysql+pymysql://root:@localhost/social_app"
# إنشاء محرك قاعدة البيانات
engine = create_engine(DATABASE_URL)

# إنشاء الجداول في قاعدة البيانات (إذا لم تكن موجودة)
Base.metadata.create_all(engine)

# إنشاء جلسة للتعامل مع قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# دالة للحصول على جلسة قاعدة البيانات
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    # مثال بسيط لاستخدام قاعدة البيانات
    from sqlalchemy.orm import Session

    def create_user(db: Session, username, password, email=None):
        db_user = User(username=username, password=password, email=email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    with SessionLocal() as db:
        new_user = create_user(db, "testuser", "password123", "test@example.com")
        print(f"تم إنشاء مستخدم جديد: {new_user.username}")