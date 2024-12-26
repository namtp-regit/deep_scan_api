from pathlib import Path
from fastapi_mail import FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader
from core.config import settings

# create environment Jinja2
template_dir = Path(__file__).resolve().parent.parent / "templates"
env = Environment(loader=FileSystemLoader(template_dir))


async def send_email(to_email: str, subject: str, body: str, is_html: bool = False):
    message = MessageSchema(
        recipients=[to_email],
        subject=subject,
        body=body,
        subtype="html" if is_html else "plain",
    )

    fm = FastMail(settings.mail_conf)
    await fm.send_message(message)

    # eg: send mail
    # await send_email(to_email, subject, body, is_html=True)


async def send_email_with_template(
    to_email: str,
    subject: str,
    template_name: str,
    template_context: dict,
):
    # Load và render template
    template = env.get_template(template_name)
    html_content = template.render(**template_context)

    # Create message schema
    message = MessageSchema(
        recipients=[to_email],
        subject=subject,
        body=html_content,
        subtype="html",
    )

    fm = FastMail(settings.mail_conf)
    await fm.send_message(message)

    # eg: send mail
    # template_context = {
    #     "name": name,
    #     "subject": subject,
    #     "body": body,
    # }

    # await send_email_with_template(
    #     to_email=to_email,
    #     subject=subject,
    #     template_name="email_template.html",
    #     template_context=template_context,
    # )
