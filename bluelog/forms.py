from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, Regexp, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(message=u'请输入正确的姓名'),Length(2,3)])
    email = StringField('email', validators=[DataRequired(message=u'请输入正确的邮箱'),Email()])
    phone = StringField('name',validators=[DataRequired(message=u'请输入正确的手机号码'),Regexp(r'1[3-9]\d{9}',message=u'请输入正确的手机号码'),])
    password = PasswordField('Password', validators=[DataRequired(message=u'请输入6-20个字符'),Length(4,20,message=u'请输入6-20个字符')])
    password2 = PasswordField('Password', validators=[DataRequired(message=u'请输入6-20个字符'),EqualTo('password','密码填写不一致')])
    submit = SubmitField('注册')

class Landed(FlaskForm):
    phone = StringField('name',validators=[DataRequired(message=u'请输入正确的手机号码'),Regexp(r'1[3-9]\d{9}',message=u'请输入正确的手机号码'),])
    password = PasswordField('Password', validators=[DataRequired(message=u'请输入6-20个字符'),Length(4,20,message=u'请输入6-20个字符')])
    submit = SubmitField('登陆')

class Major(FlaskForm):
    name = StringField('名称', validators=[DataRequired(),Length(2,15,message=u'请输入6-20个字符')])
    remarks = StringField('备注',)
    least = StringField('最少', validators=[DataRequired(), Length(1,15,message=u'请输入6-20个字符')])
    maximum = StringField('最大', validators=[DataRequired(), Length(1,15,message=u'请输入6-20个字符')])
    exegesis = TextAreaField('备注')

class Subcategory(FlaskForm):
    name = StringField('名称', validators=[DataRequired(),Length(2,15,message=u'请输入6-20个字符')])
    exegesis = TextAreaField('备注')
    major_id = SelectField('归属id',validators=[DataRequired(),Regexp(r'\d{1,3}',message=u'非法请求')])

class About(FlaskForm):
    name = TextAreaField('CMS页面内容')

class basicsettings(FlaskForm):
    title = StringField('标题', validators=[DataRequired(),Length(2,15,message=u'请输入6-20个字符')])
    Keyword = TextAreaField('关键字')
    description = TextAreaField('描述')

class csv_forms(FlaskForm):
    file_ = FileField('文件')