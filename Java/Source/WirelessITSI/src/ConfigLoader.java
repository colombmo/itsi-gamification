import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class ConfigLoader {

	@SuppressWarnings("resource")
	public String[] loadCfg(String path){
		String token = "";

		// Load configuration file.
		Scanner inFile1;
		
		try {
			inFile1 = new Scanner(new File(path)).useDelimiter(",\\s*");
			List<String> temps = new ArrayList<String>();

			// while loop
			while (inFile1.hasNext()) {
				// find next line
				token = inFile1.next();
				temps.add(token);
			}

			inFile1.close();

			String[] tempsArray = temps.toArray(new String[0]);

			return tempsArray;
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		return null;
	}
}
