
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;

/**
 * Object containing all data to be sent to the database, allows the representation as json, and handles connection and POST to database.
 * @author Moreno Colombo
 * @version 1.1
 * @since 13.06.2015
 */

public class ForwardData {

	// ---------------------------------------------------------------
	// Variables.
	// ---------------------------------------------------------------
	
	private String timestamp;
	private String sensorID;
	private String eventID;
	private String values[];
	
	// ---------------------------------------------------------------
	// Constructor.
	// ---------------------------------------------------------------
	
	/**
	 * Default Constructor.
	 */
	public ForwardData(){};
	
	/**
	 * Full Constructor.
	 */
	public ForwardData(String eventID, int sensorID, String values[], String date){		
		this.setTimestamp(date);
		this.setEventID(eventID);
		this.setSensorID(""+sensorID);
		this.setValues(values);
	}

	// ---------------------------------------------------------------
	// Getter-setters.
	// ---------------------------------------------------------------
	
	public String getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}

	public String getSensorID() {
		return sensorID;
	}

	public void setSensorID(String sensorID) {
		this.sensorID = sensorID;
	}

	public String getEventID() {
		return eventID;
	}

	public void setEventID(String eventID) {
		this.eventID = eventID;
	}

	public String[] getValues() {
		return values;
	}

	public void setValues(String values[]) {
		this.values = values;
	}
	
	// ---------------------------------------------------------------
	// Methods
	// ---------------------------------------------------------------
	/**
	 * Format the object as JSON.
	 * @return Object as JSON
	 */
	public String toJSON(){
		String jsonValue = "{\"eventID\" : " + this.getEventID() + 
						", \"sensorID\" : " + this.getSensorID() +
						", \"timeStamp\" : \"" + this.getTimestamp() + "\" ," +
						" \"tagID\" : [";

		// Add each record.
		for(int i = 0 ; i < this.getValues().length ; i++){
			if(this.getValues()[i] != null){
				jsonValue += "\"" + this.getValues()[i] + "\"";
				if(i + 1 != this.getValues().length){
					jsonValue += ", ";
				}
			}
		}
	
		// Add ending.
		jsonValue += "]}";
		return jsonValue;
	}
	
	/**
	 * Send the object formatted as JSON to the server, to be saved in the database.
	 * @param ipAddress the IP address of the server.
	 */
	public void sendToDB(String ipAddress){
		// Send information.
		HttpPost postRequest = new HttpPost("http://" + ipAddress + "/hubnet/irec/");
		postRequest.setHeader("content-type", "application/json");
		
		String jsonValue = this.toJSON();
		
		StringEntity entity;
		try {
			entity = new StringEntity(jsonValue);
			postRequest.setEntity(entity);
			HttpClient client = HttpClientBuilder.create().build();
			client.execute(postRequest);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}