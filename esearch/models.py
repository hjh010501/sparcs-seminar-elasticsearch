from django.db import models
from .search import NewaraIndex
class core_article(models.Model):
    
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    content_text = models.TextField()
    url = models.TextField()

    class Meta:
        db_table = "core_article"

    def indexing(self):
        obj = NewaraIndex(
        meta={'id': self.id},
        title=self.title,
        content=self.content,
        content_text=self.content_text,
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