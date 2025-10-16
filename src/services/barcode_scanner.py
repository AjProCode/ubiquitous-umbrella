"""Barcode scanning service"""

from typing import Optional, List, Tuple
from io import BytesIO

# Optional imports for barcode functionality
try:
    import cv2
    import numpy as np
    from pyzbar import pyzbar
    HAS_CAMERA_SUPPORT = True
except ImportError:
    HAS_CAMERA_SUPPORT = False
    np = None

try:
    import barcode
    from barcode.writer import ImageWriter
    HAS_BARCODE_GENERATION = True
except ImportError:
    HAS_BARCODE_GENERATION = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class BarcodeScanner:
    """Service for scanning and generating barcodes"""
    
    def __init__(self):
        """Initialize barcode scanner"""
        self.supported_formats = [
            'EAN13', 'EAN8', 'UPCA', 'UPCE',
            'CODE39', 'CODE128', 'ITF', 'QRCODE'
        ]
    
    def scan_from_camera(self, camera_index: int = 0, timeout: int = 30) -> Optional[str]:
        """
        Scan barcode from camera
        
        Args:
            camera_index: Camera device index
            timeout: Timeout in seconds
            
        Returns:
            Scanned barcode string or None
        """
        if not HAS_CAMERA_SUPPORT:
            raise RuntimeError("Camera support not available. Install opencv-python and pyzbar: pip install opencv-python pyzbar")
        
        cap = cv2.VideoCapture(camera_index)
        
        try:
            frame_count = 0
            max_frames = timeout * 30  # Assuming 30 FPS
            
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                # Decode barcodes in frame
                barcodes = pyzbar.decode(frame)
                
                for barcode_obj in barcodes:
                    barcode_data = barcode_obj.data.decode('utf-8')
                    return barcode_data
                
                frame_count += 1
                
        finally:
            cap.release()
        
        return None
    
    def scan_from_image(self, image_path: str) -> List[str]:
        """
        Scan barcodes from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of scanned barcode strings
        """
        if not HAS_CAMERA_SUPPORT:
            raise RuntimeError("Image scanning not available. Install opencv-python and pyzbar: pip install opencv-python pyzbar")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        barcodes = pyzbar.decode(image)
        return [barcode_obj.data.decode('utf-8') for barcode_obj in barcodes]
    
    def scan_from_array(self, image_array) -> List[str]:
        """
        Scan barcodes from numpy array (image)
        
        Args:
            image_array: Image as numpy array
            
        Returns:
            List of scanned barcode strings
        """
        if not HAS_CAMERA_SUPPORT:
            raise RuntimeError("Image scanning not available. Install opencv-python and pyzbar: pip install opencv-python pyzbar")
        
        barcodes = pyzbar.decode(image_array)
        return [barcode_obj.data.decode('utf-8') for barcode_obj in barcodes]
    
    def generate_barcode(
        self,
        barcode_data: str,
        barcode_type: str = 'EAN13',
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate barcode image
        
        Args:
            barcode_data: Data to encode
            barcode_type: Type of barcode
            output_path: Optional path to save image
            
        Returns:
            BytesIO object containing barcode image
        """
        if not HAS_BARCODE_GENERATION:
            raise RuntimeError("Barcode generation not available. Install python-barcode and pillow: pip install python-barcode pillow")
        
        if barcode_type.upper() not in self.supported_formats:
            raise ValueError(f"Unsupported barcode type: {barcode_type}")
        
        # Get barcode class
        barcode_class = barcode.get_barcode_class(barcode_type.lower())
        
        # Generate barcode
        barcode_obj = barcode_class(barcode_data, writer=ImageWriter())
        
        # Save to BytesIO or file
        if output_path:
            barcode_obj.save(output_path)
        
        buffer = BytesIO()
        barcode_obj.write(buffer)
        buffer.seek(0)
        
        return buffer
    
    def validate_barcode(self, barcode_data: str, barcode_type: str = 'EAN13') -> bool:
        """
        Validate barcode format
        
        Args:
            barcode_data: Barcode data to validate
            barcode_type: Type of barcode
            
        Returns:
            True if valid, False otherwise
        """
        if not HAS_BARCODE_GENERATION:
            # Basic validation without library
            if not barcode_data or not barcode_data.isdigit():
                return False
            return len(barcode_data) in [8, 12, 13]  # Common barcode lengths
        
        try:
            barcode_class = barcode.get_barcode_class(barcode_type.lower())
            # Try to create barcode - will raise exception if invalid
            barcode_class(barcode_data)
            return True
        except Exception:
            return False
    
    def get_barcode_info(self, image_array) -> List[Tuple[str, str, tuple]]:
        """
        Get detailed barcode information from image
        
        Args:
            image_array: Image as numpy array
            
        Returns:
            List of tuples (data, type, position)
        """
        if not HAS_CAMERA_SUPPORT:
            raise RuntimeError("Image scanning not available. Install opencv-python and pyzbar: pip install opencv-python pyzbar")
        
        barcodes = pyzbar.decode(image_array)
        
        results = []
        for barcode_obj in barcodes:
            data = barcode_obj.data.decode('utf-8')
            barcode_type = barcode_obj.type
            position = barcode_obj.rect
            results.append((data, barcode_type, position))
        
        return results
