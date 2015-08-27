import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

/**
 * Launch a thread for each sensor, get and filter data from socket and send it to the database.
 * @author Moreno Colombo
 * @version 1.0
 * @since 15.07.2015
 */

public class SocketFactory extends Thread{

	// Variables.
	private String ipAddress, eventID;
	private int port, index, sensorID;
	private long timeDiff = 0;
	
	// Constructor
	public SocketFactory(int port, String eventID, int sensorID, int index, String ipAddress, long timediff){
		this.port = port;
		this.eventID = eventID;
		this.sensorID = sensorID;
		this.index = index;
		this.ipAddress = ipAddress;
		this.timeDiff = timediff;
	}

	// Runnable.
	/* (non-Javadoc)
	 * @see java.lang.Thread#run()
	 */
	@Override
	public void run() {
		//Variables.
		String oldDate = "";
		Map <String,OldRecords> lastReads = new HashMap<String, OldRecords>();
	
		// Create Reader object, connecting to physical device

		try {	
			ServerSocket listener = new ServerSocket(port);
			Main.instances[this.index] = listener;
			
			Socket socket = listener.accept();
			
			// Console output.
			System.out.println(new Date().toString() + "> Reader " + sensorID + " created and listening"); 
			
			// Create input stream to read tag reads                	
        	BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        	PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
			
        	// JSON parser for parsing received string
        	JSONParser jsonParser = new JSONParser();
        	
        	while (Main.threadDone == false) {
        		
        		out.println("ok");
        		out.flush();
        		
        		while(!in.ready()){}
            	
            	JSONArray tagReads = (JSONArray) jsonParser.parse(in.readLine());
            	         	
            	 /*
				 *  Filter tagReads based on the number of detections
				 */
				for(int i=0; i<tagReads.size(); i++){
					JSONObject json = (JSONObject)tagReads.get(i);
					int readCount = (int)(long)json.get("readCount");
					
					if(readCount<=2){
						tagReads.remove(i);
					}
				}
								
				//Update recordings of last 3 loops by shifting 1 position to the right
				
				for (Map.Entry<String, OldRecords> entry : lastReads.entrySet()) {
				    String key = entry.getKey();
				    OldRecords value = entry.getValue();
				    value.deleteFirst();
				    lastReads.put(key, value);
				 }
				
				// Update Map with last registered elements
				
				for(int i=0; i<tagReads.size(); i++){
					String epc = (String)((JSONObject)tagReads.get(i)).get("epc");
					OldRecords tempRec = lastReads.get(epc);
					if (tempRec!=null){
						tempRec.onRead();
						lastReads.put(epc, tempRec);
					}else{
						lastReads.put(epc, new OldRecords());
					}
				}
				
				// Put tags read at least half of the last readings in an array, they will be shown on the visualization
				List<String> filteredTags = new ArrayList<String>();
				// Iterate over components of the Map
				Iterator<Map.Entry<String,OldRecords>> iter = lastReads.entrySet().iterator();
				while (iter.hasNext()) {
				    Map.Entry<String,OldRecords> entry = iter.next();
					String key = entry.getKey();
				    int sum = entry.getValue().getSum();
				    if(sum>=3){
				    	// More than half of the last readings, keep this tag
				    	filteredTags.add(key);
				    }else if(sum==0){
				    	// If empty array ({0,0,0}), delete entry from hashmap
				    	iter.remove();
				    }
				}
				String [] values = filteredTags.toArray(new String[filteredTags.size()]);
				// Records always sorted for visualization application
				Arrays.sort(values);
				synchronized(Main.records){
					Main.records.put(this.sensorID, values.clone());
				}
				
				// Send recorded values to database
				if(values.length > 0){
					// Get time.
					Calendar calendar = Calendar.getInstance();
					calendar.setTimeInMillis(new Date().getTime() - timeDiff);
					String date = TimeUtils.formatDate(calendar);
					
					// If not already sent a record in the same second, send it
					if(!date.equals(oldDate)){
						ForwardData sample = new ForwardData(eventID, sensorID, values, date);
						sample.sendToDB(ipAddress);
						// Update date of last sent record
						oldDate = date;
					}
				}
				// Restart loop.
            }
        	
        	// Close connection and terminate all of the clients
            System.out.println(new Date().toString() + "> Reader " + sensorID + " closing connection");
            out.print("terminate");
            out.flush();
            
            Thread.sleep(100);
            socket.close();
            listener.close();
        }
        catch(Exception e) {
        	System.out.println(new Date().toString() + "> Reader " + sensorID + " exception: " + e.getMessage());
        }
	}
}