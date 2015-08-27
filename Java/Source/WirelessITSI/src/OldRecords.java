/**
 * Object allowing to register the last 3 reads of one sensor and retrieving the number of detections of a tag in these reads.
 * This is used to reduce instabilities in the live visualization and detection bugs.
 * 
 * @author Moreno Colombo
 * @version 1.0
 * @since 11.06.2015
 */
public class OldRecords {
	// ---------------------------------------------------------------
	// Variables.
	// ---------------------------------------------------------------
	private int reads;
	
	// ---------------------------------------------------------------
	// Constructor.
	// ---------------------------------------------------------------
	/**
	 * Constructor.
	 */
	public OldRecords(){
		this.reads = 16; // 0b10000
	}
	
	// ---------------------------------------------------------------
	// Methods.
	// ---------------------------------------------------------------
	/**
	 * Change last reading, by shifting everything to the right by one position.
	 */
	public void deleteFirst(){
		this.reads = this.reads >> 1; // Shift right
	}
	
	/**
	 * Register reading of an element in the current reading loop.
	 */
	public void onRead(){
		this.reads = 16|this.reads; // 0b10000|reads
	}
	
	/**
	 * Count the number of bits in the {@code reads} variable.
	 * @return The number of detections in the last 5 readings.
	 */
	public int getSum(){
		return Integer.bitCount(this.reads);
	}
}
