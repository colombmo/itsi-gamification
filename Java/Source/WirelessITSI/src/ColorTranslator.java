import java.awt.Color;


public class ColorTranslator {
	/**
	 * Translate hexadecimal code of a color into a Color object.
	 * @param hexstring a string containing the hexadecimal code of a color
	 * @return A color
	 */
	public static Color parseStringToColor(String hexstring){
		int i = Integer.parseInt(hexstring,16);
		Color color = new Color(i);
		return color;
	}		
}
