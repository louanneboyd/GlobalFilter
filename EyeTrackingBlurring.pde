import java.io.File;

int blurLevels = 20;
float clarityBoost = 2.3;
int maxBlur = 7;

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
    blurs[i] = blur(img, (int)(i*((float)maxBlur/blurLevels)));
    //image(blurs[i], i*500, 0);  
  }
  color[] newImage = heatmap.pixels;
  for (int i = 0; i < newImage.length; ++i)
  {
    int heatmapBrightness = (int)red(newImage[i]);
    int blurLevel = (blurLevels - 1) - min((int)(clarityBoost * heatmapBrightness) * (blurLevels) / 255, blurLevels - 1);
    if (blurLevel == 0)
    {
      newImage[i] = blurs[blurLevel].pixels[i];
    } else
    {
      float lerpFactor = (heatmapBrightness % ((float)255 / blurLevels)) / ((float)255 / blurLevels);
      //println(lerpFactor);
      newImage[i] = lerpColor(blurs[blurLevel].pixels[i], blurs[blurLevel-1].pixels[i], lerpFactor);
    }
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
