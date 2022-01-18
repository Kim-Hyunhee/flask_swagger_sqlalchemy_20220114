from server import db

class Feeds(db.Model):
    __tablename__ = 'feeds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # users테이블의 id컬럼으로 가는 외래키.
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id')) # null이면, 특정 강의에 대한 글 아님.
    content = db.Column(db.TEXT, nullable=False) # TEXT 컬럼 대응
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    # 외래키로 설정된 관계를 ORM으로 표현해보자.
    writer = db.relationship('Users')
    lecture = db.relationship('Lectures')
    
    # ORM으로 관계 표현 (SQLAlchemy)의 정석 => 부모의 입장에서 자식 목록을 갖고 있자
    # backref => 자식 테이블 모델의 입장에서 본인을 찾아올 때 사용할 변수의 이름을 지정
    feed_images = db.relationship('FeedImages', backref= 'feed')
    
    
    def get_data_object(self, need_writer=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'lecture_id': self.lecture_id,
            'content': self.content,
            'created_at': str(self.created_at),
            'images' : [ fi.get_data_object() for fi in self.feed_images ]
        }
        
        
        # 이 글의 작성자가 누군인지 알수 있다면, json을 만들때마다 자동 첨부되면 편하겠다.
        if need_writer:
            data['writer'] = self.writer.get_data_object()
        
        # 이 글이 어느 강의에 대해 쓰인 것인지 첨부
        data['lecture'] = self.lecture.get_data_object()
        
        return data