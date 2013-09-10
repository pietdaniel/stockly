from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight



# lol deprecated functions
import random, crypt, string
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor, md5_constructor
def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return md5_constructor(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


# Tutorial shit
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
class Snippet(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets')
    highlighted = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='python',
                                max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly',
                             max_length=100)

    class Meta:
        ordering = ('created',)


    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


class Stock(models.Model):
    name =  models.CharField(max_length=64, blank=True, default='')
    price = models.DecimalField(max_digits=10,decimal_places=5)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('updated',)
        permissions = (
            ("can_update", "can update"),
        )


class Client(models.Model):
    name = models.CharField(max_length=64, blank=True, default='')
    password = models.CharField(max_length=254)

    def set_password(self, raw_password):
        import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, self.password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)
        super(Client, self).save(*args, **kwargs)

    class Meta:
        permissions = (
            ("can_update", "Can update"),
        )


class StockList(models.Model):
    sl_owner = models.ForeignKey(Client, related_name='sl_owner')
    stocks = models.ManyToManyField(Stock, related_name='stocks')


class FriendList(models.Model):
    owner = models.ForeignKey(Client, related_name='owner')
    friends = models.ManyToManyField(Client, related_name='friends')
