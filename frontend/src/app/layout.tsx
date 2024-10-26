import './globals.css'

export const metadata = {
  title: 'Dropfarm',
  description: 'Automation Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
}