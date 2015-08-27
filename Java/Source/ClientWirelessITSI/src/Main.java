import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.thingmagic.Reader;
import com.thingmagic.TMConstants;
import com.thingmagic.TagReadData;

/**
 * Program to be executed on each of the computers connected to a reader.
 * This reads tags next to a sensor and sends them back to the server in JSON format.
 * @author Moreno Colombo
 * @version 2.0
 * @since 15.07.2015
 */
public class Main {
	@SuppressWarnings("unchecked")
	public static void main(String[] args){
		// Variables.
		Reader reader;
		String serverAddress, comPort;
		int port;
	
		//Variables.
		TagReadData[] tagReads;
		
		// Create Reader object, connecting to physical device
		try{		
			/**
			 *  Load configuration file (containing server address, com port and socket port)
			 */
			String token;
			Scanner inFile = new Scanner(new File("default.cfg"));
			inFile.useDelimiter(",\\s*");
			List<String> temps = new ArrayList<String>();

			while (inFile.hasNext()) {
				// find next line
				token = inFile.next();
				temps.add(token);
			}
			inFile.close();
			String[] tempsArray = temps.toArray(new String[0]);
			
			serverAddress = tempsArray[0];
			comPort = tempsArray[1];
			port = Integer.parseInt(tempsArray[2]);
			
			/**
			 *  Create reader, connect and configure
			 */
			reader = Reader.create("tmr:///" + comPort);
			reader.connect();
	
			if (Reader.Region.UNSPEC == (Reader.Region)reader.paramGet("/reader/region/id")){
				Reader.Region[] supportedRegions = (Reader.Region[])reader.paramGet(TMConstants.TMR_PARAM_REGION_SUPPORTEDREGIONS);
				if (supportedRegions.length < 1){
					try {
						throw new Exception("Reader doesn't support any regions");
					} catch (Exception e) {}
				}
				else{
					reader.paramSet("/reader/region/id", supportedRegions[0]);
				}
			}
			
			// Connect to a socket
			Socket s = new Socket(serverAddress, port);
			
			// Create output stream to send reads and input to get instructions on what to do from the server
			BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
			PrintWriter out = new PrintWriter(s.getOutputStream(), true);

			/**
			 *  Read tags and send to server to be treated until the server doesn't terminate the connections
			 */
			while(!in.readLine().equals("terminate")){
				
				// Read tags
				tagReads = reader.read(400);
								
				// Create JSON array to be sent
				JSONArray data = new JSONArray();
				
				// Put records in a JSON array
				for(int i=0; i<tagReads.length; i++){
					JSONObject obj = new JSONObject();
					obj.put("epc", new String(tagReads[i].epcString()));
					obj.put("readCount", new Integer(tagReads[i].getReadCount()));
					data.add(obj);
				}
								
				// Send records in JSON array via socket to server
				out.println(data.toString());				
				out.flush();
			}
			/**
			 *  When received termination signal, close socket connection and finish program
			 */
			in.close();
			out.close();
			s.close();
			reader.destroy();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}