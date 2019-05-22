PImage originalImage;
PImage img;
void setup() {
  background(0);
  String imageName = "girl.jpg"; 
  img = loadImage(imageName); 
  originalImage = loadImage(imageName);
  //image(img, 0, 0);
  size(500,700);
  noLoop();
  
}

void draw()
{
  image(blur(img, 50), 0, 0);
}


PImage edgeDetect(PImage img, int amount)
{
  PImage blurred = img.get();
  PImage original = img.get();
  blurred.filter(BLUR, amount);
  //image(blurred, img.width, 0);
  //image(original, 2*img.width, 0);
  blurred.filter(INVERT);
  original.blend(blurred, 0, 0, img.width, img.height, 0, 0, img.width, img.height, ADD);
  return original;
}

PImage blur(PImage img, int amount)
{
  PImage newImg = img.get();
  newImg.filter(BLUR, amount);
  return newImg;
}
