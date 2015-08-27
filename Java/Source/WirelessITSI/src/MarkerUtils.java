import java.io.IOException;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;

@SuppressWarnings("deprecation")
public class MarkerUtils {
	public static void recordMarker(String ipAddress, int eventID, String label){
		try {
			@SuppressWarnings("resource")
			HttpClient client = new DefaultHttpClient();
			String markerText = label.replace(" ", "%20");
			HttpPost postRequest = new HttpPost("http://" + ipAddress + "/hubnet/mrkr/" + eventID + "/" + markerText);
			
			client.execute(postRequest);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
