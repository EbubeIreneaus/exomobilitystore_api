from django.conf import settings
from ninja.router import Router
from schemas.order import OrderSchema
from django.core.mail import send_mail, EmailMultiAlternatives

router = Router()

@router.post('')
def post_order(request, body: OrderSchema):
    try:

        rows = ""
        for item in body.items:
            rows += f"""
                <tr>
                    <td style="padding:8px;border:1px solid #ddd;">{item.name}</td>
                    <td style="padding:8px;border:1px solid #ddd;">${item.discount:.2f}</td>
                    <td style="padding:8px;border:1px solid #ddd;">{item.quantities}</td>
                </tr>
            """
        
        html_body = f"""
        <html>
          <body style="font-family:Arial,sans-serif;color:#333;">
            <h2 style="color:#2563eb;">New Order</h2>

            <p><strong>Name:</strong> {body.name}</p>
            <p><strong>Email:</strong> {body.email}</p>
            <p><strong>Country:</strong> {body.country}</p>
            <p><strong>City:</strong> {body.city}</p>
            <p><strong>Address:</strong> {body.address}</p>

            <h3 style="margin-top:20px;">Products</h3>

            <table style="border-collapse:collapse;width:100%;max-width:600px;">
              <thead>
                <tr style="background:#f1f5f9;">
                  <th style="padding:8px;border:1px solid #ddd;text-align:left;">
                    Product
                  </th>
                  <th style="padding:8px;border:1px solid #ddd;text-align:left;">
                    Discount
                  </th>
                  <th style="padding:8px;border:1px solid #ddd;text-align:left;">
                    Quantity
                  </th>
                </tr>
              </thead>
              <tbody>
                {rows}
              </tbody>
            </table>
          </body>
        </html>
        """

        subject = "New Order Received"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = [
            "support@exomobilitystore.com",
        ]

        email = EmailMultiAlternatives(
            subject=subject,
            body="You have received a new order.",
            from_email=from_email,
            to=recipients,
        )

        email.attach_alternative(html_body, "text/html")
        email.send()

        customer_subject = "Your Order Has Been Received – Exo Mobility Store"
        customer_body = f"""
Hi {body.name},

Thank you for shopping with Exo Mobility Store!

Your order has been received and is being processed. 
A confirmation has been sent to our team, and we will notify you once your order is shipped.

If you do not see our emails, please check your spam or junk folder.

Thank you for choosing Exo Mobility Store!

Best regards,
The Exo Mobility Store Team
"""

        try:
            send_mail(
            subject=customer_subject,
            message=customer_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[body.email],
            fail_silently=True,
            )
        except Exception as e:
            pass

        return {"success": True}
    except Exception as e:
        print(str(e))
        return {"success": False, "error": 'unknown server error! try again later'}