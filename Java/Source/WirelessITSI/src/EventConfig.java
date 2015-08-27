import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;

/**
 * Class that handles the calls to the server to get informations about the event and the participants.
 * @author Moreno Colombo
 *
 */

public class EventConfig {

	/**
	 * Get informations about the tables at the event
	 * @param ipAddress The address of the server
	 * @param event	The id of the current event
	 * @return An array of tables
	 */
	public static Table[] getEnvironment(String ipAddress, int event){

		try {
			// Get tables from server for this event
			HttpClient client = HttpClientBuilder.create().build();
			HttpGet getRequest = new HttpGet("http://" + ipAddress + "/hubnet/getTables/"+event);
			HttpResponse response;
			String token = "";
			
			response = client.execute(getRequest);
			BufferedReader br = new BufferedReader(new InputStreamReader((response.getEntity().getContent())));
			String res = br.readLine();
			
			Scanner in = new Scanner(res);
			in.useDelimiter(":&:");
			List<String> temps = new ArrayList<String>();
			
			// while loop
			while (in.hasNext()) {
				// find next line
				token = in.next();
				temps.add(token);
			}
			
			List<Table> tables = new ArrayList<Table>();
			
			for(int i=0; i<temps.size(); i+=4){
				tables.add(new Table(Integer.parseInt(temps.get(i)),temps.get(i+1),(int)Float.parseFloat(temps.get(i+2)),(int)Float.parseFloat(temps.get(i+3))));
			}
			Table[] tempsArray = tables.toArray(new Table[0]);
			in.close();
			
			return tempsArray;
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}
	
	/**
	 * Get informations about the participants at the event
	 * @param ipAddress The address of the server
	 * @param event	The id of the current event
	 * @return A Map of couples {@code (participantId, color)}
	 */
	public static Map<String,Participant> getParticipants(String ipAddress, int event){

		try {
			// Get tables from server for this event
			HttpClient client = HttpClientBuilder.create().build();
			HttpGet getRequest = new HttpGet("http://" + ipAddress + "/hubnet/getParticipants/"+event);
			HttpResponse response;
			String token = "";
			
			response = client.execute(getRequest);
			BufferedReader br = new BufferedReader(new InputStreamReader((response.getEntity().getContent())));
			String res = br.readLine();
			
			Scanner in = new Scanner(res);
			in.useDelimiter(":&:");
			List<String> temps = new ArrayList<String>();
			
			// while loop
			while (in.hasNext()) {
				// find next line
				token = in.next();
				temps.add(token);
			}
			
			Map<String,Participant> parts = new HashMap<String,Participant>();
			
			for(int i=0; i<temps.size(); i+=5){
				parts.put(temps.get(i), new Participant(temps.get(i+1),temps.get(i+2), temps.get(i+3), Integer.parseInt(temps.get(i+4))));
			}
			in.close();
			
			return parts;
			
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}
	
	/**
	 * Get informations about the interests for the event
	 * @param ipAddress The address of the server
	 * @param event	The id of the current event
	 * @return An array of interests
	 */
	
	public static Interest[] getInterests(String ipAddress, int event){
		try {
			// Get tables from server for this event
			HttpClient client = HttpClientBuilder.create().build();
			HttpGet getRequest = new HttpGet("http://" + ipAddress + "/hubnet/getInterests/"+event);
			HttpResponse response;
			String token = "";
			
			response = client.execute(getRequest);
			BufferedReader br = new BufferedReader(new InputStreamReader((response.getEntity().getContent())));
			String res = br.readLine();
			Scanner in = new Scanner(res);
			in.useDelimiter(":&:");
			List<String> temps = new ArrayList<String>();
			
			// while loop
			while (in.hasNext()) {
				// find next line
				token = in.next();
				temps.add(token);
			}
			
			List<Interest> ints = new ArrayList<Interest>();
			
			for(int i=0; i<temps.size(); i+=2){
				ints.add(new Interest(temps.get(i), temps.get(i+1)));
			}
			Interest[] tempsArray = ints.toArray(new Interest[0]);
			in.close();
			
			return tempsArray;
			
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}
}
