'use client'

import { useState } from 'react'
import { Bell, Package, Truck, Users, BarChart as BarChartIcon, PieChart, TrendingUp, FileText, AlertTriangle, Clock, Fuel, MapPin, Map as MapIcon, Activity, ClipboardList, Brain } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Bar, BarChart, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Placeholder Map Component
const MapPlaceholder = () => (
  <div className="relative w-full h-[300px] bg-gray-100 rounded-lg overflow-hidden">
    <div className="absolute inset-0 flex items-center justify-center">
      <MapIcon className="h-16 w-16 text-gray-400" />
    </div>
    <div className="absolute bottom-4 left-4 bg-white p-2 rounded shadow">
      <div className="flex items-center space-x-2">
        <div className="w-3 h-3 bg-blue-500 rounded-full" />
        <span className="text-sm font-medium">Truck Location</span>
      </div>
      <div className="flex items-center space-x-2 mt-1">
        <div className="w-3 h-3 bg-green-500 rounded-full" />
        <span className="text-sm font-medium">Destination</span>
      </div>
    </div>
  </div>
)

export default function Dashboard() {
  const [notifications, setNotifications] = useState([
    { id: 1, message: "Shipment #1234 has been delayed", isRead: false },
    { id: 2, message: "New task assigned: Update inventory", isRead: false },
    { id: 3, message: "Shipment #5678 has arrived at the destination", isRead: true },
  ])

  const markAsRead = (id: number) => {
    setNotifications(notifications.map(notif => 
      notif.id === id ? { ...notif, isRead: true } : notif
    ))
  }

  const mockMISData = [
    { id: "T001", route: "Ahmedabad - Ajmer - Jaipur", distance: 450, capacityUtilization: 90, deliveries: 5, fuelConsumption: 15, driverName: "Ram Kumar", departureTime: "08:00 AM", arrivalTime: "03:30 PM", plannedStops: 2, unplannedStops: 1, geofencingAlerts: 1, vehicleCondition: "Maintenance Due" },
    { id: "T002", route: "Mumbai - Pune", distance: 150, capacityUtilization: 75, deliveries: 3, fuelConsumption: 12, driverName: "Suresh Patel", departureTime: "09:00 AM", arrivalTime: "12:00 PM", plannedStops: 1, unplannedStops: 0, geofencingAlerts: 0, vehicleCondition: "Good" },
    { id: "T003", route: "Delhi - Chandigarh", distance: 240, capacityUtilization: 85, deliveries: 4, fuelConsumption: 13, driverName: "Arjun Mehra", departureTime: "06:30 AM", arrivalTime: "11:00 AM", plannedStops: 2, unplannedStops: 0, geofencingAlerts: 0, vehicleCondition: "Service Completed" },
    { id: "T004", route: "Kolkata - Patna", distance: 500, capacityUtilization: 80, deliveries: 6, fuelConsumption: 18, driverName: "Sanjay Singh", departureTime: "05:00 AM", arrivalTime: "03:00 PM", plannedStops: 3, unplannedStops: 1, geofencingAlerts: 2, vehicleCondition: "Good" },
    { id: "T005", route: "Hyderabad - Bangalore", distance: 570, capacityUtilization: 95, deliveries: 7, fuelConsumption: 17, driverName: "Anil Sharma", departureTime: "07:00 AM", arrivalTime: "05:00 PM", plannedStops: 2, unplannedStops: 0, geofencingAlerts: 1, vehicleCondition: "Maintenance Due" },
  ]

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Logistics Dashboard</h1>
      
      {/* Summary Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Shipments</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,234</div>
            <p className="text-xs text-muted-foreground">+20.1% from last month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Drivers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">56</div>
            <p className="text-xs text-muted-foreground">+3 since yesterday</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">On-Time Delivery</CardTitle>
            <Truck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94.2%</div>
            <p className="text-xs text-muted-foreground">+2.4% from last week</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <BarChartIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$52,234</div>
            <p className="text-xs text-muted-foreground">+15.3% from last month</p>
          </CardContent>
        </Card>
      </div>

      {/* Shipment Tracking Section */}
      <Card className="mb-8">
        <CardHeader className="flex flex-row items-center space-x-2">
          <Truck className="h-6 w-6" />
          <CardTitle>Real-Time Shipment Tracking</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span>Shipment #1234</span>
                  <Badge>In Transit</Badge>
                </div>
                <Progress value={60} className="w-full" />
                <p className="text-sm text-muted-foreground mt-1">Estimated arrival: 2 days</p>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span>Shipment #5678</span>
                  <Badge variant="outline">Delivered</Badge>
                </div>
                <Progress value={100} className="w-full" />
                <p className="text-sm text-muted-foreground mt-1">Arrived at destination</p>
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span>Shipment #9012</span>
                  <Badge variant="secondary">Preparing</Badge>
                </div>
                <Progress value={20} className="w-full" />
                <p className="text-sm text-muted-foreground mt-1">Estimated departure: 1 day</p>
              </div>
            </div>
            <div>
              <MapPlaceholder />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Task Management Section */}
      <Card className="mb-8">
        <CardHeader className="flex flex-row items-center space-x-2">
          <ClipboardList className="h-6 w-6" />
          <CardTitle>Task Management</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-4">
            <li className="flex items-center justify-between">
              <span>Update inventory for Warehouse A</span>
              <Button size="sm">Complete</Button>
            </li>
            <li className="flex items-center justify-between">
              <span>Schedule maintenance for Truck #789</span>
              <Button size="sm">Complete</Button>
            </li>
            <li className="flex items-center justify-between">
              <span>Review and approve new shipping routes</span>
              <Button size="sm">Complete</Button>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* MIS Phase - Data Analysis and Reporting */}
      <Card className="mb-8">
        <CardHeader className="flex flex-row items-center space-x-2">
          <Activity className="h-6 w-6" />
          <CardTitle>Management Information System</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <h3 className="text-lg font-semibold mb-2">Key Metrics</h3>
              <ul className="space-y-2">
                <li className="flex items-center justify-between">
                  <span>Average Fuel Efficiency</span>
                  <Badge variant="secondary">8.5 L/100km</Badge>
                </li>
                <li className="flex items-center justify-between">
                  <span>Route Deviation Instances</span>
                  <Badge variant="secondary">12</Badge>
                </li>
                <li className="flex items-center justify-between">
                  <span>Vehicle Downtime</span>
                  <Badge variant="secondary">3.2%</Badge>
                </li>
                <li className="flex items-center justify-between">
                  <span>Truck Utilization Rate</span>
                  <Badge variant="secondary">87%</Badge>
                </li>
                <li className="flex items-center justify-between">
                  <span>On-Time Performance</span>
                  <Badge variant="secondary">94.5%</Badge>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">Generate Reports</h3>
              <div className="space-y-2">
                <Select>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select report type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fleet">Fleet Performance</SelectItem>
                    <SelectItem value="fuel">Fuel Consumption</SelectItem>
                    <SelectItem value="route">Route Optimization</SelectItem>
                    <SelectItem value="driver">Driver Performance</SelectItem>
                  </SelectContent>
                </Select>
                <Button className="w-full">
                  <FileText className="mr-2 h-4 w-4" />
                  Generate Report
                </Button>
              </div>
            </div>
          </div>
          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Data Visualization</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Route Deviation Trends</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center h-48">
                    <TrendingUp className="h-32 w-32 text-muted-foreground" />
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Fuel Consumption Comparison</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center h-48">
                    <BarChartIcon className="h-32 w-32 text-muted-foreground" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Live Geofencing Alerts</h3>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Truck ID</TableHead>
                  <TableHead>Driver</TableHead>
                  <TableHead>Alert Type</TableHead>
                  <TableHead>Time</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell>TRK-001</TableCell>
                  <TableCell>John Doe</TableCell>
                  <TableCell>
                    <Badge variant="destructive">Route Deviation</Badge>
                  </TableCell>
                  <TableCell>10:23 AM</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>TRK-005</TableCell>
                  <TableCell>Jane Smith</TableCell>
                  <TableCell>
                    <Badge variant="warning">Unplanned Stop</Badge>
                  </TableCell>
                  <Table Cell>11:45 AM</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Predictive Insights</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Peak Load Times</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center">
                    <Clock className="h-8 w-8 text-muted-foreground mr-2" />
                    <span>2:00 PM - 4:00 PM</span>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Next Maintenance Due</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center">
                    <Truck className="h-8 w-8 text-muted-foreground mr-2" />
                    <span>TRK-003 in 2 days</span>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Suggested Route Change</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center">
                    <MapPin className="h-8 w-8 text-muted-foreground mr-2" />
                    <span>Route A to B: -5km</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
          
          {/* New MIS Report Visualization Section */}
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-2">MIS Report: Fleet Performance Visualization</h3>
            <Card>
              <CardHeader>
                <CardTitle>Truck Performance Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={mockMISData}>
                    <XAxis dataKey="id" />
                    <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
                    <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
                    <Tooltip />
                    <Legend />
                    <Bar yAxisId="left" dataKey="distance" fill="#8884d8" name="Distance (km)" />
                    <Bar yAxisId="left" dataKey="capacityUtilization" fill="#82ca9d" name="Capacity Utilization (%)" />
                    <Bar yAxisId="right" dataKey="fuelConsumption" fill="#ffc658" name="Fuel Consumption (L/100 km)" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      {/* Notification System */}
      <Card>
        <CardHeader className="flex flex-row items-center space-x-2">
          <Bell className="h-6 w-6" />
          <CardTitle>Notifications</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[200px]">
            <ul className="space-y-4">
              {notifications.map((notif) => (
                <li key={notif.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Bell className={`h-4 w-4 ${notif.isRead ? 'text-muted-foreground' : 'text-blue-500'}`} />
                    <span className={notif.isRead ? 'text-muted-foreground' : ''}>{notif.message}</span>
                  </div>
                  {!notif.isRead && (
                    <Button size="sm" variant="outline" onClick={() => markAsRead(notif.id)}>
                      Mark as Read
                    </Button>
                  )}
                </li>
              ))}
            </ul>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  )
}