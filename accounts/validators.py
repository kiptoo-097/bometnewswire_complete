from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO

def validate_social_image_dimensions(image, platform='facebook'):
    """
    Main validation function that all others will use
    Validates image dimensions and aspect ratio for social media platforms
    """
    required_dimensions = {
        'facebook': (1200, 630),
        'twitter': (1200, 675),
        'whatsapp': (1200, 630),
        'general': (1200, 630)
    }
    
    try:
        if hasattr(image, 'temporary_file_path'):
            # Temporary uploaded file
            with Image.open(image.temporary_file_path()) as img:
                width, height = img.size
        else:
            # In-memory uploaded file
            with Image.open(BytesIO(image.read())) as img:
                width, height = img.size
            image.seek(0)  # Reset file pointer
        
        req_width, req_height = required_dimensions.get(platform, (1200, 630))
        
        # Check minimum dimensions
        if width < req_width or height < req_height:
            raise ValidationError(
                f'Image too small. For {platform}, minimum size is {req_width}x{req_height} pixels. '
                f'Uploaded image is {width}x{height}.'
            )
            
        # Check aspect ratio (with 10% tolerance)
        aspect = width / height
        ideal_aspect = req_width / req_height
        if abs(aspect - ideal_aspect) > 0.1:
            raise ValidationError(
                f'Image aspect ratio should be close to {req_width}:{req_height} for {platform}. '
                f'Current aspect ratio is {width}:{height} ({aspect:.2f}).'
            )
            
    except IOError:
        raise ValidationError("Unable to read image file")
    except Exception as e:
        raise ValidationError(f"Error validating image: {str(e)}")

# Platform-specific validator functions
def validate_general_image(image):
    """Validator for general social media images"""
    return validate_social_image_dimensions(image, 'general')

def validate_facebook_image(image):
    """Validator for Facebook-optimized images"""
    return validate_social_image_dimensions(image, 'facebook')

def validate_twitter_image(image):
    """Validator for Twitter-optimized images"""
    return validate_social_image_dimensions(image, 'twitter')

def validate_whatsapp_image(image):
    """Validator for WhatsApp-optimized images"""
    return validate_social_image_dimensions(image, 'whatsapp')