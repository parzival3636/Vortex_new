# QR Verification WebApp

Separate frontend for vendor and receiver dashboards with QR-based verification.

## Features

- 🏢 **Vendor Dashboard**: Monitor loads, generate QR codes, track verifications
- 📦 **Receiver Dashboard**: Scan QR codes, verify deliveries, receive notifications
- 🚚 **Driver Scanner**: Display QR codes for pickup and delivery
- 🤖 **AI Integration**: Real-time verification with confidence scores
- 🔔 **Live Notifications**: Instant updates on verification events

## Tech Stack

- React 18
- Vite
- TailwindCSS
- React Router
- QRCode.react (QR generation)
- html5-qrcode (QR scanning)
- Axios (API calls)
- Lucide React (icons)

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

Runs on: http://localhost:5174

## Build

```bash
npm run build
```

## Project Structure

```
src/
├── pages/
│   ├── LandingPage.jsx       # Role selection and login
│   ├── VendorDashboard.jsx   # Vendor load management
│   ├── ReceiverDashboard.jsx # Receiver QR scanning
│   └── DriverScanner.jsx     # Driver QR display
├── services/
│   └── api.js                # API integration
├── App.jsx                   # Router configuration
└── main.jsx                  # Entry point
```

## API Configuration

Backend URL: `http://localhost:8001/api/v1`

Configure in `src/services/api.js`

## Routes

- `/` - Landing page with role selection
- `/vendor/:vendorId` - Vendor dashboard
- `/receiver/:receiverId` - Receiver dashboard
- `/driver/scan/:loadId` - Driver QR scanner

## Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8001/api/v1
```

## Usage

### Vendor Flow

1. Login with vendor ID
2. View assigned loads
3. Click "Generate Pickup QR"
4. QR code displayed on dashboard
5. Track verification status in real-time
6. Receive notifications on pickup/delivery

### Receiver Flow

1. Login with receiver ID
2. View incoming loads
3. Click "Start Scanning"
4. Scan driver's QR code
5. AI verifies delivery
6. Confirmation displayed

### Driver Flow

1. Access `/driver/scan/:loadId`
2. QR code displayed automatically
3. Show QR to vendor (pickup) or receiver (delivery)
4. Wait for verification
5. Proceed to next step

## Key Components

### VendorDashboard
- Load list with status badges
- QR code generation
- Real-time verification tracking
- Notification panel
- Quick stats

### ReceiverDashboard
- Camera-based QR scanner
- Incoming loads list
- Verification results
- Notification feed
- Instructions panel

### DriverScanner
- Large QR code display
- Status timeline
- Context-aware instructions
- Load details

## Styling

Uses TailwindCSS with custom configuration:

- Primary color: Indigo
- Status colors: Yellow (assigned), Blue (awaiting), Purple (transit), Green (delivered)
- Responsive design for mobile and desktop

## Browser Support

- Chrome 90+ (recommended for QR scanning)
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### QR Scanner not working
- Ensure HTTPS or localhost
- Grant camera permissions
- Try Chrome browser

### API connection failed
- Check backend is running on port 8001
- Verify CORS settings
- Check network tab in DevTools

### QR code not displaying
- Check load has QR generated
- Verify API response
- Check console for errors

## License

MIT
