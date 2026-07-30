import os

import qrcode


QR_FOLDER = "qr_codes"


def create_qr_folder():
    """Create the QR code storage folder if needed."""
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)


def generate_box_qr(box_id, location=None):
    """Generate a QR code for a herbarium box.

    Parameters:
        box_id (str): Unique box identifier
        location (str): Physical location of box

    Returns:
        str: Path to generated QR image
    """
    create_qr_folder()

    if location:
        qr_data = (
            f"Herbarium Twin\n"
            f"Box ID: {box_id}\n"
            f"Location: {location}"
        )
    else:
        qr_data = f"Herbarium Twin\nBox ID: {box_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image()
    filepath = os.path.join(QR_FOLDER, f"{box_id}.png")
    img.save(filepath)

    return filepath