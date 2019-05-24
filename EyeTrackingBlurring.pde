import java.io.File;

int blurLevels = 10;
float clarityBoost = 1.3;
int maxBlur = 40;

File directoryImages;
File directoryHeatmaps;
File [] images;
File [] heatmaps;

void setup() {
  directoryImages = new File(dataPath("input/images"));
  directoryHeatmaps = new File(dataPath("input/heatmaps"));
  images = directoryImages.listFiles();
  heatmaps = directoryHeatmaps.listFiles();
  
  background(0);
  //image(img, 0, 0);
  size(1,1);
  noLoop();
}

void draw()
{
  for (int i = 0; i < images.length; ++i)
  {
    println("image: " + images[i]);
    PImage img = loadImage(images[i].toString());
    PImage heatmap = loadImage(heatmaps[i].toString());
    PImage result = heatmapBlur(img, heatmap);
    result.save("data/output/" + images[i].getName());
    println("file saved: data/output/" + images[i].getName());
  }
}

PImage heatmapBlur(PImage img, PImage heatmap)
{
  PImage blurs [] = new PImage[blurLevels];
  for (int i = 0; i < blurLevels; ++i)
  {
    blurs[i] = blur(img, i*(maxBlur/blurLevels));
    //image(blurs[i], i*500, 0);  
  }
  color[] newImage = heatmap.pixels;
  for (int i = 0; i < newImage.length; ++i)
  {
    int blurLevel = (blurLevels - 1) - min((int)(clarityBoost * red(newImage[i])) * blurLevels / 255, blurLevels - 1);
    newImage[i] = blurs[blurLevel].pixels[i];
  }
  PImage result = createImage(img.width, img.height, RGB);
  result.pixels = newImage;
  return result;
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
