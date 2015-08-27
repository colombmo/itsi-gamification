import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.Toolkit;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import javax.swing.JFrame;
import javax.swing.JPanel;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;
/**
 * Class drawing and updating the live visualization based on the data recorded.
 * @author Moreno Colombo
 * @version 1.0
 * @since 08.07.2015
 */
public class IndividualView extends JPanel implements Runnable {
	
	// ---------------------------------------------------------------
	// Variables.
	// ---------------------------------------------------------------	
	private static JFrame frame;
	Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize(); // Get size of the screen to fill it with the visualization
	private static final long serialVersionUID = 1L;					// Prevent a warning 
	
	private String ipAddress;
	private int eventId;
	
	private FontMetrics fm;
	
	private final int WIDTH = screenSize.width;							// The width of the screen
	private final int HEIGHT = screenSize.height-40;					// The height of the screen
	private Table[] tables;												// Array containing the tables and their characteristics
	protected Map<String,Participant> parts;								// Hashmap containing informations about the participants of the event
	protected int maxScore = 1;
	private Interest[] inters;											// Array containing the color of the interests
	
	protected static boolean flag = true;									// Flag to know when to stop the drawing
	
	// ---------------------------------------------------------------
	// Constructor.
	// ---------------------------------------------------------------
		
	public IndividualView(Table[] t, Map<String,Participant> p, Interest[] i, String ipAddress, int eventId){
		this.tables = t;
		this.parts = p;
		this.inters = i;
		this.ipAddress = ipAddress;
		this.eventId = eventId;
	};	
	
	// ---------------------------------------------------------------
	// Methods.
	// ---------------------------------------------------------------
	/**
	 * Draws the legend for the live visualization.
	 * @param g A Graphics environment object
	 */
	private void drawLegend(Graphics g){
		Graphics2D g2d = (Graphics2D) g;
		int leftMargin = (WIDTH / 100);
		int topMargin = HEIGHT -(HEIGHT / 10);
		int fontSize = WIDTH / 90;
		int tabulation = leftMargin;
		
		// Draw the bar.
		g.setColor(Color.black);
		g2d.fillRect(0, HEIGHT-(HEIGHT/10), WIDTH, HEIGHT/10);
		
		g.setFont(new Font(g.getFont().getFontName(),Font.BOLD,fontSize));
		
		// Draw the legends.
		for (int i=0; i<inters.length;i++){
			// Get appropriate color.
			Color tagColor = ColorTranslator.parseStringToColor(inters[i].getColor());
			
			// Draw color tag and text.
			g.setColor(tagColor);
			g2d.fillRect(tabulation, topMargin + (HEIGHT/100), (HEIGHT / 22), (HEIGHT / 22));
			
			g.setColor(Color.white);
			g.drawString(inters[i].getDescription(), tabulation + (HEIGHT / 20), topMargin + (HEIGHT / 25)); 

			tabulation += g.getFontMetrics().stringWidth(inters[i].getDescription()) + (HEIGHT / 10);
		}
	}
	
	public void drawRoom(Graphics g){
		int[] xPoints = {WIDTH/2-20, WIDTH/2+20, WIDTH/2};
		int[] yPoints = {70,70,30};
		g.setColor(Color.RED);	
		g.fillPolygon(xPoints, yPoints, 3);
	}
	
	/**
	 * Draw the slices of pie around the tables and the tables themselves.
	 * @param g A Graphics environment object
	 */
	public void drawPieGraph(Graphics g){
		Graphics2D g2d = (Graphics2D) g;
		g.setFont(new Font(g.getFont().getFontName(),Font.BOLD,12));
		fm = g.getFontMetrics();
		
		for (int i=0; i<tables.length; i++){
			// Set position of pie graph and table
			int tX = tables[i].getX()*WIDTH/100;
			int tY = tables[i].getY()*HEIGHT/100;			
			String[] temp = Main.records.get(tables[i].getId());
				if (temp!=null && temp.length>0){
					int angle = (int)360.0/temp.length;
					for (int j=0; j<temp.length; j++){
						int size = (int)(((double)parts.get(temp[j]).getScore())/((double)maxScore)*200);
						// If user is in the first 3 positions
						int position = parts.get(temp[j]).getPosition();
						if(position > 0 && position <= 3){
							// Draw slice of pie														
							g.setColor(getCol(temp[j]));
							g2d.fillArc(tX-size/2, tY-size/2, size, size, j*angle, angle);
							
							int x = ((j+0.5)*angle>=270 || (j+0.5)*angle<=90)?tX:tX-fm.stringWidth(getName(temp[j]));
							
							// Show name of user
							g.setFont(new Font(g.getFont().getFontName(),Font.BOLD,22));
							if(position == 1){
								g.setColor(Color.ORANGE);
							}else if(position == 2){
								g.setColor(new Color(127, 140, 141));
							}else{
								g.setColor(new Color(211, 84, 0));
							}
							g2d.drawString("★", (int)(x+(size/2+20)*Math.sin((j+0.5)*angle*Math.PI/180+Math.PI/2))+fm.stringWidth(getName(temp[j])), (int)(tY+(size/2+20)*Math.cos((j+0.5)*angle*Math.PI/180+Math.PI/2)));
							g.setFont(new Font(g.getFont().getFontName(),Font.BOLD,12));
							
							g2d.drawString(getName(temp[j]), (int)(x+(size/2+20)*Math.sin((j+0.5)*angle*Math.PI/180+Math.PI/2)), (int)(tY+(size/2+20)*Math.cos((j+0.5)*angle*Math.PI/180+Math.PI/2)));
							
						}else{
							// Draw slice of pie
							g.setColor(getCol(temp[j]));
							g2d.fillArc(tX-size/2, tY-size/2, size, size, j*angle, angle);
							
							// Show initials of user
							g.setColor(Color.BLACK);
							int x = ((j+0.5)*angle>=270 || (j+0.5)*angle<=90)?tX:tX-fm.stringWidth(getInitials(temp[j]));
							g2d.drawString(getInitials(temp[j]), (int)(x+(size/2+20)*Math.sin((j+0.5)*angle*Math.PI/180+Math.PI/2)), (int)(tY+(size/2+20)*Math.cos((j+0.5)*angle*Math.PI/180+Math.PI/2)));
						}
					}
			}
			// Draw table
			g.setColor(Color.black);
			g2d.fillOval(tX-8, tY-8, 16, 16);
		}
	}
	
	/**
	 * Get score of all of the participants
	 */
	
	public void updateScores(){
		// Get interests and scores from server for this event
		HttpClient client = HttpClientBuilder.create().build();
		HttpGet getRequest = new HttpGet("http://" + ipAddress + "/hubnet/getScores1/"+eventId);
		HttpResponse response;
		String token = "";
		
		try {
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
			
			for(int i=0; i<temps.size(); i+=2){
				parts.get(temps.get(i)).setScore(Integer.parseInt(temps.get(i+1)));
				parts.get(temps.get(i)).setPosition(i/2+1);
			}
			maxScore = parts.get(temps.get(0)).getScore();
			in.close();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	private String getInitials(String rec){
		Participant part = this.parts.get(rec);
		String first = part.getFirstName().substring(0, 1);
		String last = part.getLastName().substring(0, 1);
		return first+last;
	}
	
	private String getName(String rec){
		Participant part = this.parts.get(rec);
		String first = part.getFirstName();
		String last = part.getLastName();
		return first+" "+last;
	}
	
	/**
	 * Get color of participants
	 * @param rec
	 * @return
	 */
	private Color getCol(String rec){
		String colorStr = this.parts.get(rec).getColor();
		if(colorStr!=null) return ColorTranslator.parseStringToColor(colorStr);
		else return Color.white;
	}
	
	@Override
	public void paint(Graphics g) {
		super.paint(g);
		Graphics2D g2d = (Graphics2D) g;
		g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
				RenderingHints.VALUE_ANTIALIAS_ON);
		
		drawLegend(g);
		drawRoom(g);
		drawPieGraph(g);
	}
	
	public void run() {	
		flag = true;
		frame = new JFrame("Individual live visualization");
		IndividualView liveVis = new IndividualView(tables, parts, inters, ipAddress, eventId);
		frame.add(liveVis);
		frame.setSize(WIDTH, HEIGHT);
		frame.setVisible(true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		liveVis.setBackground(Color.WHITE);
		
		(new Thread(new UpdateScore(liveVis))).start();
		
		while (flag) {
			liveVis.repaint();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	/**
	 * Kill drawing thread.
	 */
	public static void kill(){
		flag = false;
		frame.setVisible(false);
		frame.dispose(); //Destroy the JFrame object
	}
}
