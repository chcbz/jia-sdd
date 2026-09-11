import cn.jia.core.util.OpenCvUtil;
import cn.jia.core.util.OcrUtil;
import java.awt.image.BufferedImage;
import java.nio.file.Path;
import javax.imageio.ImageIO;
public class PublicImageProbe {
 public static void main(String[] args) throws Exception {
  Path root=Path.of(args[0]);
  BufferedImage image=new BufferedImage(16,16,BufferedImage.TYPE_INT_RGB);
  for(int y=0;y<16;y++) for(int x=0;x<16;x++) image.setRGB(x,y, x<8 ? 0x101010 : 0xf0f0f0);
  var input=root.resolve("fixture.png").toFile(); ImageIO.write(image,"png",input);
  var output=root.resolve("threshold.png").toFile();
  OpenCvUtil.threshold(input.toString(),output.toString());
  var actual=ImageIO.read(output);
  if(actual==null || actual.getWidth()!=16 || (actual.getRGB(2,2)&0xffffff)!=0 || (actual.getRGB(12,2)&0xffffff)!=0xffffff) throw new AssertionError("threshold mismatch");
  var tiff=OcrUtil.createImage(input,"png"); var roundTrip=ImageIO.read(tiff);
  if(roundTrip==null || roundTrip.getWidth()!=16 || roundTrip.getHeight()!=16) throw new AssertionError("TIFF dimension mismatch");
  for(int y=0;y<16;y++) for(int x=0;x<16;x++) if(image.getRGB(x,y)!=roundTrip.getRGB(x,y)) throw new AssertionError("TIFF pixel mismatch");
  System.out.println("PASS OpenCvUtil.threshold native image round trip; OcrUtil.createImage TIFF 256 pixels exact; OpenCV="+org.opencv.core.Core.VERSION);
 }
}
