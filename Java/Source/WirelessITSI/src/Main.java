import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.events.SelectionListener;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.FileDialog;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Menu;
import org.eclipse.swt.widgets.MenuItem;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;

public class Main {

	// -----------------------------------------------------------------------------
	// Variables.
	// -----------------------------------------------------------------------------

	private static int eventId;
	private static SocketFactory[] readers;
	public static ServerSocket[] instances;
	private static long timeDiff;
	private static ExecutorService executor;
	public static boolean threadDone = false;
	private static Button buttonStart;
	private static Button buttonStop;
	private static Text console;
	private static Text serverIP;
	private static Label serverIPLabel;
	private static Label markerLabel;
	private static Text markerText;
	private static Button buttonMarker;
	private static String configurationPath = "default.cfg";
	
	//Array to store all last recordings
	public static Map<Integer,String[]> records;
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// Prepare GUI.
		final Display display = new Display ();
		final Shell shell = new Shell(display);
		shell.setText("Reader Controller");
		shell.setMinimumSize(new Point(720, 670));

		// -----------------------------------------------------------------------------
		// Server settings.
		// -----------------------------------------------------------------------------

		serverIP = new Text(shell, 1);
		serverIP.setBounds(360, 0, 360, 25);
		serverIP.setText("127.0.0.1");
		serverIP.setToolTipText("The IP address of the web service host.");
		serverIPLabel = new Label(shell, 1);
		serverIPLabel.setText("Server IP Address");
		serverIPLabel.setBounds(0, 0, 360, 25);
		
		// -----------------------------------------------------------------------------
		// Marker setter.
		// -----------------------------------------------------------------------------

		markerLabel = new Label(shell, 1);
		markerLabel.setText("Time Marker");
		markerLabel.setBounds(0, 520, 360, 20);
		markerText = new Text(shell, 1);
		markerText.setToolTipText("Type in the label of the new time marker to add.");
		markerText.setBounds(0, 545, 360, 25);
		buttonMarker = new Button(shell, 1);
		buttonMarker.setText("Add Marker");
		buttonMarker.setBounds(360, 545, 360, 25);
		
		buttonMarker.addSelectionListener(new SelectionListener() {
			public void widgetSelected(SelectionEvent event) {
				if(markerText.getText() != ""){	
					MarkerUtils.recordMarker(serverIP.getText(), 3, markerText.getText());
					markerText.setText("");
				}
				else{
					System.out.println("> No text was set for the marker.");
				}
			}

			public void widgetDefaultSelected(SelectionEvent event) {}
		});
		
		// -----------------------------------------------------------------------------
		// Buttons.
		// -----------------------------------------------------------------------------

		// Display buttons for starting to read.
		buttonStart = new Button(shell, SWT.PUSH);
		buttonStart.setText("Start Reading");
		buttonStart.setSize(360, 70);
		buttonStart.setBounds(0, 50, 360, 70);

		buttonStart.addSelectionListener(new SelectionListener() {
			public void widgetSelected(SelectionEvent event) {
				startReading();
			}

			public void widgetDefaultSelected(SelectionEvent event) {}
		});

		// Display buttons for stopping to read.
		buttonStop = new Button(shell, SWT.PUSH);
		buttonStop.setText("Stop Reading");
		buttonStop.setEnabled(false);
		buttonStop.setSize(360, 70);
		buttonStop.setBounds(360, 50, 360, 70);

		buttonStop.addSelectionListener(new SelectionListener() {
			public void widgetSelected(SelectionEvent event) {
				stopReading();
			}

			public void widgetDefaultSelected(SelectionEvent event) {}
		});

		// -----------------------------------------------------------------------------
		// File menu.
		// -----------------------------------------------------------------------------

		Menu menuBar = new Menu(shell, SWT.BAR);
		MenuItem fileMenuHeader = new MenuItem(menuBar, SWT.CASCADE);
		fileMenuHeader.setText("&File");

		Menu fileMenu = new Menu(shell, SWT.DROP_DOWN);
		fileMenuHeader.setMenu(fileMenu);

		// Save log.
		MenuItem fileSaveLogItem = new MenuItem(fileMenu, SWT.PUSH);
		fileSaveLogItem.setText("Save Log\tCTRL+S");
		fileSaveLogItem.setAccelerator(SWT.CTRL + 'S');

		fileSaveLogItem.addSelectionListener(new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent arg0) {
				// Open save dialog.
				FileDialog dialog = new FileDialog(shell, SWT.SAVE);
				dialog.setFilterNames(new String[] {"All Files (*.*)"});
				dialog.setFilterExtensions(new String[] { "*.log", "*.txt", "*.*"});
				dialog.setFileName(Calendar.getInstance().toString() + ".log");

				// Save file.
				try {
					File log = new File(dialog.open());
					FileWriter fileWriter = new FileWriter(log);
					System.out.println(new Date().toString() + "> Log saved");
					fileWriter.write(console.getText());
					fileWriter.close();
					
				} catch (IOException e) {
					System.out.println(new Date().toString() + "> " + e);
				}
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent arg0) {}
		});

		// Load configuration.
		MenuItem fileLoadItem = new MenuItem(fileMenu, SWT.PUSH);
		fileLoadItem.setText("&Load config\tCTRL+L");
		fileLoadItem.setAccelerator(SWT.CTRL + 'L');

		class Open implements SelectionListener {
			public void widgetSelected(SelectionEvent event) {
				FileDialog fd = new FileDialog(shell, SWT.OPEN);
				fd.setText("Open");
				fd.setFilterPath("C:/");
				String[] filterExt = {"*.cfg"};
				fd.setFilterExtensions(filterExt);
				String selected = fd.open();
				configurationPath = selected;
				System.out.println(new Date().toString() + "> Configuation file loaded: " + selected);
			}

			public void widgetDefaultSelected(SelectionEvent event) {}
		}

		fileLoadItem.addSelectionListener(new Open());

		// Exit.
		MenuItem fileExitItem = new MenuItem(fileMenu, SWT.PUSH);
		fileExitItem.setText("E&xit\tCTRL+W");
		fileExitItem.setAccelerator(SWT.CTRL + 'W');

		fileExitItem.addSelectionListener(new SelectionListener() {
			@Override
			public void widgetSelected(SelectionEvent arg0) {
				stopReading(); shell.close(); display.dispose();
			}
			@Override
			public void widgetDefaultSelected(SelectionEvent arg0) {
				stopReading(); shell.close(); display.dispose();
			}
		});

		// -----------------------------------------------------------------------------
		// Console output.
		// -----------------------------------------------------------------------------

		console = new Text(shell, SWT.MULTI | SWT.BORDER | SWT.WRAP | SWT.V_SCROLL | SWT.READ_ONLY);
		console.setSize(720, 390);
		console.setBounds(0, 120, 720, 390);

		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		PrintStream ps = new PrintStream(baos);
		String consoleOutput = "";

		// IMPORTANT: Save the old System.out!
		//PrintStream old = System.out;

		// Tell Java to use your special stream
		System.setOut(ps);

		// -----------------------------------------------------------------------------
		// Pack GUI.
		// -----------------------------------------------------------------------------

		shell.setMenuBar(menuBar);
		shell.setSize(720, 510);
		shell.open ();

		while (!shell.isDisposed ()) {
			if (!display.readAndDispatch ()){ display.sleep ();}

			if(! baos.toString().equals(consoleOutput)){
				console.setText(baos.toString());
				consoleOutput = baos.toString();
			}
		}

		display.dispose ();
	}

	public static void startReading(){
		// Adapt GUI.
		buttonStart.setEnabled(false);
		buttonStop.setEnabled(true);

		// Load the reader configuration from file.
		threadDone = false;
		ConfigLoader loader = new ConfigLoader();
		String[] config = loader.loadCfg(configurationPath);
		
		eventId = Integer.parseInt(config[1]);
		
		// Get time difference with server (to avoid having each reader performing requests).
		timeDiff = TimeUtils.getDifference(serverIP.getText());
		
		// Create one daemons for each reader and start reading on all readers.
		int numberOfReaders = config.length / 3;
		executor = Executors.newFixedThreadPool(numberOfReaders+1);

		// Initialize records hashmap
		records = new HashMap<Integer,String[]>();
		
		readers = new SocketFactory[numberOfReaders];
		instances =  new ServerSocket[numberOfReaders];
		int argsCount = 0;	
		
		//Get tables
		Table[]tables = EventConfig.getEnvironment(serverIP.getText(), eventId);
		// Get participants
		Map<String,Participant> participants = EventConfig.getParticipants(serverIP.getText(), eventId);
		// Get interests
		Interest[] interests = EventConfig.getInterests(serverIP.getText(), eventId);
		
		for(int i = 0 ; i < readers.length ; i++){
			System.out.println("Executing readerFactory");
			int sensorId = Integer.parseInt(config[argsCount +2]);
			executor.execute(new SocketFactory(Integer.parseInt(config[argsCount]), config[argsCount +1], sensorId, i, serverIP.getText(), timeDiff));
			// Initialize entry for this reader in the records hashmap
			records.put(sensorId, null);
			argsCount += 3;
		}
		
		executor.execute(new IndividualView(tables, participants, interests, serverIP.getText(), eventId));
	}

	public static void stopReading(){
		buttonStop.setEnabled(false);

		if(instances.length > 0){
			threadDone = true;
			IndividualView.kill();
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			executor.shutdownNow();

			// Wait until the executor is done.
			while (!executor.isTerminated()) {}

			for(int i = 0 ; i < instances.length; i++){
				try {
					instances[i].close();
				} catch (IOException e) {e.printStackTrace();}
			}
		}

		buttonStart.setEnabled(true);
	}
}