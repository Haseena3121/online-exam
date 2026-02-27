import * as tf from '@tensorflow/tfjs';
import * as cocoSsd from '@tensorflow-models/coco-ssd';

class ProctoringService {
  constructor() {
    this.cocoModel = null;
    this.violations = [];
  }

  // Load models
  async loadModels() {
    try {
      console.log('Loading COCO-SSD model...');
      this.cocoModel = await cocoSsd.load();
      console.log('COCO-SSD model loaded');

      return true;
    } catch (error) {
      console.error('Error loading models:', error);
      return false;
    }
  }

  // Detect face visibility (simplified version)
  async detectFace(videoElement) {
    if (!this.cocoModel) {
      console.warn('Models not loaded yet');
      return { faceDetected: false, confidence: 0 };
    }

    try {
      const predictions = await this.cocoModel.detect(videoElement);
      const person = predictions.find(p => p.class === 'person' && p.score > 0.5);
      
      return {
        faceDetected: !!person,
        confidence: person ? person.score : 0
      };
    } catch (error) {
      console.error('Face detection error:', error);
      return { faceDetected: false, confidence: 0 };
    }
  }
  async detectFaces(videoElement) {
    if (!this.facemeshModel || !videoElement) return false;

    try {
      const predictions = await this.facemeshModel.estimateFaces(videoElement);
      return predictions.length > 0;
    } catch (error) {
      console.error('Error detecting faces:', error);
      return false;
    }
  }

  // Detect multiple persons
  async detectMultiplePersons(videoElement) {
    if (!this.cocoModel || !videoElement) return false;

    try {
      const predictions = await this.cocoModel.estimateObjects(videoElement);
      
      // Count number of people detected
      const peopleCount = predictions.filter(p => p.class === 'person').length;
      
      return peopleCount > 1; // Return true if more than 1 person
    } catch (error) {
      console.error('Error detecting persons:', error);
      return false;
    }
  }

  // Detect head position (looking away)
  async detectHeadPosition(videoElement) {
    if (!this.facemeshModel || !videoElement) return false;

    try {
      const predictions = await this.facemeshModel.estimateFaces(videoElement);
      
      if (predictions.length === 0) return false;

      const face = predictions[0];
      const keypoints = face.landmarks;

      // Check if face is looking at screen
      // This is a simplified check based on face orientation
      const noseTip = keypoints[0];
      const forehead = keypoints[10];
      
      // Check vertical deviation
      const verticalDeviation = Math.abs(noseTip[1] - forehead[1]);
      
      return verticalDeviation > 50; // Return true if looking away significantly
    } catch (error) {
      console.error('Error detecting head position:', error);
      return false;
    }
  }

  // Analyze brightness (detect low light)
  analyzeBrightness(videoElement) {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      
      ctx.drawImage(videoElement, 0, 0);
      
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;
      
      let brightness = 0;
      for (let i = 0; i < data.length; i += 4) {
        brightness += (data[i] + data[i + 1] + data[i + 2]) / 3;
      }
      
      brightness = brightness / (data.length / 4);
      
      return brightness < 50; // Return true if too dark
    } catch (error) {
      console.error('Error analyzing brightness:', error);
      return false;
    }
  }

  // Capture screenshot
  captureScreenshot(videoElement) {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      
      ctx.drawImage(videoElement, 0, 0);
      
      return new Promise(resolve => {
        canvas.toBlob(blob => {
          resolve(blob);
        }, 'image/jpeg', 0.8);
      });
    } catch (error) {
      console.error('Error capturing screenshot:', error);
      return null;
    }
  }

  // Record violation
  recordViolation(type, severity, description) {
    this.violations.push({
      type,
      severity,
      description,
      timestamp: new Date()
    });
  }

  // Get violations
  getViolations() {
    return this.violations;
  }

  // Clear violations
  clearViolations() {
    this.violations = [];
  }

  // Check for unusual sound
  async detectSound(audioContext) {
    try {
      if (!audioContext) return false;

      // Get audio analyser
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      
      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      analyser.getByteFrequencyData(dataArray);
      
      // Calculate average volume
      const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
      
      // Return true if volume is unusually high
      return average > 100;
    } catch (error) {
      console.error('Error detecting sound:', error);
      return false;
    }
  }
}

// Create singleton instance
const proctoringService = new ProctoringService();

export default proctoringService;