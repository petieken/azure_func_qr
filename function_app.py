import azure.functions as func
import logging
from qrcodegen import QrCode
from qrcodegen_util import to_svg_str

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="generateqr")
def generateqr(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    qr_text = req.params.get('content')
    if not qr_text:
        return func.HttpResponse(
            "No content was provided for generating a QR code\nProvide content with the 'content' parameter in the URL",
            status_code=400
        )

    if qr_text:
        try:
            qr0 = QrCode.encode_text(qr_text, QrCode.Ecc.QUARTILE)
            svg = to_svg_str(qr0, 1)
            return func.HttpResponse(
                svg,
                status_code=200,
                mimetype="image/svg+xml"
            )
        except Exception as e:
            logging.exception(f"Error occurred: {e}")
            return func.HttpResponse(
                f"Error occurred during generation of the QR code:\n{e}",
                status_code=400
            )
