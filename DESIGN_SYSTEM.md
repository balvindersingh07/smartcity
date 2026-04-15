# Premium Smart City Dashboard Design System

## Visual Language

- **UI style:** dark futuristic interface, glassmorphism surfaces, neon accents, soft 3D depth.
- **Background:** layered gradient anchored at `#0B0F1A`.
- **Card base:** `rgba(255,255,255,0.08)` with blur and reflective inner highlight.
- **3D feel:** layered drop shadows + inset highlights + hover elevation.
- **Corner radius scale:** `14px`, `18px`, `24px`.

## Color Tokens

- **Background:** `#0B0F1A`
- **Primary Glow:** `#4FD1C5`
- **Secondary:** `#7F5AF0`
- **Danger:** `#FF4D4F`
- **Warning:** `#FFC857`
- **Success:** `#2ECC71`
- **Text Primary:** `#EDF2FF`
- **Text Secondary:** `#9FB0D4`

## Typography

- **Primary:** Inter (`300-800`)
- **Display/Section headings:** Poppins (`500-700`)
- **Weight usage:**
  - Heading: bold
  - Data value: semibold to bold
  - Labels/meta: light to medium

## Layout System

- **Shell:** fixed left sidebar + top navbar + grid main content.
- **Main section order:**
  1. Top Navbar
  2. 4 Metric cards
  3. Map + Alerts panel
  4. 3 Chart cards
  5. Sensors table + Notification panel
- **Responsive breakpoints:**
  - `<=1220px`: compact icon-first sidebar
  - `<=1040px`: stack content into single column
  - `<=760px`: mobile/tablet friendly vertical structure

## Reusable Components

1. **Metric Card**
   - Props: `label`, `value`, `unit`, `icon`, `trend`, `status`
   - Includes status pill, trend capsule, 3D icon tile, hover glow border

2. **Sidebar Item**
   - Props: `icon`, `label`, `active`
   - States: default / hover / active with neon glow

3. **Map Sensor Marker**
   - Props: `x`, `y`, `status`, `id`, `zone`, `telemetry`
   - Neon marker with pulse animation
   - Click opens floating map tooltip card

4. **Map Tooltip Card**
   - Props: `sensorId`, `zone`, `aqi`, `temp`, `humidity`, `noise`, `status`
   - Glass 3D floating panel with semantic status chip

5. **Chart Container**
   - Props: `title`, `subtitle`, `type`
   - Dark chart grid, smooth curves, neon gradients

6. **Alert Item**
   - Props: `level`, `title`, `message`, `time`
   - Variants:
     - `critical` red glow + pulse
     - `warning` yellow
     - `normal` green

7. **Notification Toast**
   - Props: `title`, `message`
   - Stacked floating notifications with auto-dismiss

8. **Data Table Row**
   - Props: `sensorId`, `zone`, `status`, `lastSync`
   - Status badges: success / warning / danger

## Motion & Effects

- Metric card hover elevation and glow.
- Neon pulse animation for sensor markers.
- Critical alert pulse animation for urgency.
- Toast slide-in transition.
- Subtle ambient glow orbs in background.

## Data Shapes

- `metric`: `{ key, label, value, unit, icon, trend, status }`
- `sensor`: `{ id, zone, x, y, aqi, temp, humidity, noise, status, sync }`
- `alert`: `{ title, message, level, time }`
- `notification`: `{ title, text }`

## Accessibility Notes

- High contrast text against dark surfaces.
- Marker interactions use semantic buttons.
- Alerts carry color and text cues for severity.
- Responsive layout preserves hierarchy and spacing.
