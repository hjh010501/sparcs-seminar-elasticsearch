from django.db import models
from .search import NewaraIndex
class core_article(models.Model):
    
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    commented_at = models.DateTimeField()
    content = models.TextField()
    content_text = models.TextField()
    is_anonymous = models.IntegerField()
    is_content_sexual = models.IntegerField()
    is_content_social = models.IntegerField()
    positive_vote_count = models.IntegerField()
    negative_vote_count = models.IntegerField()
    created_by_id = models.IntegerField()
    parent_board_id = models.IntegerField()
    parent_topic_id = models.IntegerField()
    url = models.TextField()

    class Meta:
        db_table = "core_article"

    def indexing(self):
        obj = NewaraIndex(
        meta={'id': self.id},
        created_at=self.created_at,
        updated_at=self.updated_at,
        deleted_at=self.deleted_at,
        commented_at=self.commented_at,
        title=self.title,
        content=self.content,
        content_text=self.content_text,
        is_anonymous=self.is_anonymous,
        is_content_sexual=self.is_content_sexual,
        is_content_social=self.is_content_social,
        positive_vote_count=self.positive_vote_count,
        negative_vote_count=self.negative_vote_count,
        created_by_id=self.created_by_id,
        parent_board_id=self.parent_board_id,
        parent_topic_id=self.parent_topic_id,
        url=self.url,
        )
        obj.save()
        return obj.to_dict(include_meta=True)

class Search(models.Lookup):
   lookup_name = 'search'

   def as_mysql(self, compiler, connection):
       lhs, lhs_params = self.process_lhs(compiler, connection)
       rhs, rhs_params = self.process_rhs(compiler, connection)
       params = lhs_params + rhs_params
       return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params


models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)