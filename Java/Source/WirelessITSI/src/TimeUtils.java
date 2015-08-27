import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

/**
 * 
 * @author Thomas Rouvinez
 * 
 * Description: class that handles the calls and computation of time difference between the
 * 				client and the server. This avoids having each reader perform requests each 
 * 				second on the server.
 *
 */
@SuppressWarnings("deprecation")
public class TimeUtils {

	@SuppressWarnings("null")
	public static long getDifference(String ipAddress){

		try {
			// Get server time.
			@SuppressWarnings("resource")
			HttpClient client = new DefaultHttpClient();
			HttpGet getRequest = new HttpGet("http://" + ipAddress + "/hubnet/time/0");
			HttpResponse response;
			
			// Compute request time.
			long start = System.currentTimeMillis();
			
			response = client.execute(getRequest);
			BufferedReader br = new BufferedReader(new InputStreamReader((response.getEntity().getContent())));
			String tempTime = br.readLine();
			DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.ENGLISH);
			Date serverTime = format.parse(tempTime);
			Date systemTime = new Date();
			
			long stop = System.currentTimeMillis();
			
			// Get time difference.
			long diffInMillis = serverTime.getTime() - systemTime.getTime() - (stop - start);
			
			System.out.println(new Date().toString()+ "> Server time: " + serverTime.toString());
			System.out.println(new Date().toString() + "> System time: " + systemTime.toString());
			System.out.println(new Date().toString() + "> Time difference: " + diffInMillis + " ms");
			
			return diffInMillis;
		} catch (IOException | ParseException e) {
			e.printStackTrace();
			return (Long) null;
		}
	}
	
	public static String formatDate(Calendar calendar){
		SimpleDateFormat customFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		
		return customFormat.format(calendar.getTime());
	}
}
