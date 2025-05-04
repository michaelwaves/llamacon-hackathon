"use client"

import type React from "react"

import { useState, useRef, ChangeEvent, FormEvent } from "react"
import { Upload, Phone, MessageSquare, Mail, User, AlertCircle, CheckCircle, XCircle, HelpCircle, Image as ImageIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { motion, AnimatePresence } from "framer-motion"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

// Types
type TransactionStatus = "approved" | "flagged" | "review"
type Transaction = {
  id: string
  amount: string
  status: TransactionStatus
  forwardedTo: string
  timestamp: string
  merchant?: string
  category?: string
  riskScore?: number
}

export default function Home() {
  const [isUploading, setIsUploading] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [logs, setLogs] = useState<{ text: string; color: string }[]>([])
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [overallStatus, setOverallStatus] = useState<"idle" | "safe" | "review" | "fraud">("idle")
  const fileInputRef = useRef<HTMLInputElement>(null)

  // State for the new profile analysis form
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [occupation, setOccupation] = useState("")
  const [textField1, setTextField1] = useState("")
  const [textField2, setTextField2] = useState("")
  const [textField3, setTextField3] = useState("")
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [profileAnalysisResult, setProfileAnalysisResult] = useState<{ description: string; riskScore: number } | null>(null)
  const [isAnalyzingProfile, setIsAnalyzingProfile] = useState(false)
  const profileImageInputRef = useRef<HTMLInputElement>(null)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setLogs([])
    setTransactions([])
    setOverallStatus("idle")

    // Simulate file upload
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setIsUploading(false)
    setIsAnalyzing(true)

    // Simulate log entries with timed appearance and colors
    const logEntries = [
      { text: "Parsing CSV file...", color: "text-blue-400" },
      { text: "Validating transaction data format...", color: "text-blue-400" },
      { text: "Scanning transaction patterns...", color: "text-green-400" },
      { text: "Detected recurring charge from flagged merchant...", color: "text-amber-400" },
      { text: "Analyzing transaction velocity...", color: "text-purple-400" },
      { text: "Launching AI risk assessment module...", color: "text-cyan-400" },
      { text: "Generating risk scores for each transaction...", color: "text-pink-400" },
      { text: "Cross-referencing with known fraud patterns...", color: "text-red-400" },
      { text: "Analysis complete. Displaying results.", color: "text-green-500" },
    ]

    for (let i = 0; i < logEntries.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 700))
      setLogs((prev) => [...prev, logEntries[i]])
    }

    // Simulate API call to analyze transactions
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Sample transaction data
    const sampleTransactions: Transaction[] = [
      {
        id: "TX12345",
        amount: "$149.99",
        status: "approved",
        forwardedTo: "Archive",
        timestamp: "2023-05-15 14:32:45",
        merchant: "Amazon",
        category: "Retail",
        riskScore: 12,
      },
      {
        id: "TX12346",
        amount: "$299.50",
        status: "flagged",
        forwardedTo: "Security Team",
        timestamp: "2023-05-15 15:47:22",
        merchant: "Unknown Vendor",
        category: "Electronics",
        riskScore: 87,
      },
      {
        id: "TX12347",
        amount: "$1,250.00",
        status: "review",
        forwardedTo: "Customer Support",
        timestamp: "2023-05-15 16:03:11",
        merchant: "Transfer",
        category: "Financial",
        riskScore: 64,
      },
      {
        id: "TX12348",
        amount: "$79.99",
        status: "approved",
        forwardedTo: "Archive",
        timestamp: "2023-05-15 16:15:30",
        merchant: "Netflix",
        category: "Subscription",
        riskScore: 8,
      },
      {
        id: "TX12349",
        amount: "$5,000.00",
        status: "flagged",
        forwardedTo: "Fraud Department",
        timestamp: "2023-05-15 16:22:45",
        merchant: "International Transfer",
        category: "Financial",
        riskScore: 92,
      },
      {
        id: "TX12350",
        amount: "$24.99",
        status: "approved",
        forwardedTo: "Archive",
        timestamp: "2023-05-15 16:30:12",
        merchant: "Spotify",
        category: "Subscription",
        riskScore: 5,
      },
    ]

    setTransactions(sampleTransactions)
    setIsAnalyzing(false)

    // Determine overall status
    const hasFraud = sampleTransactions.some((t) => t.status === "flagged")
    const hasReview = sampleTransactions.some((t) => t.status === "review")

    if (hasFraud) {
      setOverallStatus("fraud")
    } else if (hasReview) {
      setOverallStatus("review")
    } else {
      setOverallStatus("safe")
    }
  }

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImageFile(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    } else {
      setImageFile(null)
      setImagePreview(null)
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  const triggerProfileImageInput = () => {
    profileImageInputRef.current?.click()
  }

  const handleProfileSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!firstName || !lastName || !occupation || !imageFile) {
      // Basic validation - add more as needed
      alert("Please fill in First Name, Last Name, Occupation, and upload an image.")
      return
    }

    setIsAnalyzingProfile(true)
    setProfileAnalysisResult(null)

    const formData = new FormData()
    formData.append("firstName", firstName)
    formData.append("lastName", lastName)
    formData.append("occupation", occupation)
    formData.append("textField1", textField1)
    formData.append("textField2", textField2)
    formData.append("textField3", textField3)
    formData.append("image", imageFile)

    try {
      // TODO: Replace with the actual backend endpoint URL
      const response = await fetch("/api/analyze_profile", { // ASSUMED ENDPOINT
        method: "POST",
        body: formData,
        // Headers might not be needed if backend handles FormData correctly
        // headers: { 'Content-Type': 'multipart/form-data' }, // Let browser set this with boundary
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setProfileAnalysisResult(result) // Assuming backend returns { description: string, riskScore: number }

    } catch (error) {
      console.error("Error submitting profile analysis:", error)
      // TODO: Show user-friendly error message
      alert("Failed to analyze profile. Please try again.")
      setProfileAnalysisResult({ description: "Error during analysis.", riskScore: -1 }) // Example error state
    } finally {
      setIsAnalyzingProfile(false)
    }
  }

  const needsAction = transactions.some((t) => t.status === "flagged" || t.status === "review")

  const getStatusBadge = (status: TransactionStatus) => {
    switch (status) {
      case "approved":
        return (
          <div className="flex items-center gap-1.5">
            <CheckCircle className="h-4 w-4 text-green-500" />
            <span className="text-green-700 font-medium">Archived</span>
          </div>
        )
      case "flagged":
        return (
          <div className="flex items-center gap-1.5">
            <XCircle className="h-4 w-4 text-red-500" />
            <span className="text-red-700 font-medium">Security Ops AI</span>
          </div>
        )
      case "review":
        return (
          <div className="flex items-center gap-1.5">
            <HelpCircle className="h-4 w-4 text-amber-500" />
            <span className="text-amber-700 font-medium">Customer AI Avatar Interview</span>
          </div>
        )
      default:
        return null
    }
  }

  const getRiskScoreBadge = (score: number) => {
    let colorClass = "bg-green-100 text-green-800"
    if (score > 80) {
      colorClass = "bg-red-100 text-red-800"
    } else if (score > 50) {
      colorClass = "bg-amber-100 text-amber-800"
    } else if (score > 30) {
      colorClass = "bg-blue-100 text-blue-800"
    }

    return <Badge className={`${colorClass} rounded-full px-2 py-0.5 text-xs font-medium`}>{score}</Badge>
  }

  const getOverallStatusAlert = () => {
    switch (overallStatus) {
      case "safe":
        return (
          <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-6 rounded-r-md">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              <p className="text-green-700 font-medium">All Transactions Safe</p>
            </div>
          </div>
        )
      case "review":
        return (
          <div className="bg-amber-50 border-l-4 border-amber-500 p-4 mb-6 rounded-r-md">
            <div className="flex items-center">
              <HelpCircle className="h-5 w-5 text-amber-500 mr-2" />
              <p className="text-amber-700 font-medium">Review Required</p>
            </div>
          </div>
        )
      case "fraud":
        return (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-md">
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
              <p className="text-red-700 font-medium">Possible Fraud Detected</p>
            </div>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <main className="container mx-auto px-4 py-8 max-w-6xl space-y-8">
      <Card className="mb-8 border-none shadow-lg">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-2xl font-bold">AI-Powered Transaction Analyzer</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 dark:bg-gray-900 dark:border-gray-700">
            <input type="file" ref={fileInputRef} onChange={handleFileUpload} accept=".csv" className="hidden" />
            <Upload className="h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium mb-2">Upload Transaction CSV</h3>
            <p className="text-sm text-gray-500 mb-4 text-center">
              Drag and drop your CSV file here, or click to browse
            </p>
            <Button
              onClick={triggerFileInput}
              disabled={isUploading || isAnalyzing}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {isUploading ? "Uploading..." : "Select CSV File"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* New Profile Analysis Card */}
      <Card className="border-none shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Profile Risk Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleProfileSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="firstName">First Name</Label>
                <Input id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
              </div>
              <div>
                <Label htmlFor="lastName">Last Name</Label>
                <Input id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
              </div>
            </div>
            <div>
              <Label htmlFor="occupation">Occupation</Label>
              <Input id="occupation" value={occupation} onChange={(e) => setOccupation(e.target.value)} required />
            </div>
            <div>
              <Label htmlFor="textField1">Additional Info 1</Label>
              <Textarea id="textField1" value={textField1} onChange={(e) => setTextField1(e.target.value)} />
            </div>
            <div>
              <Label htmlFor="textField2">Additional Info 2</Label>
              <Textarea id="textField2" value={textField2} onChange={(e) => setTextField2(e.target.value)} />
            </div>
            <div>
              <Label htmlFor="textField3">Additional Info 3</Label>
              <Textarea id="textField3" value={textField3} onChange={(e) => setTextField3(e.target.value)} />
            </div>
            <div>
              <Label>Profile Image</Label>
              <div className="flex items-center gap-4 mt-2">
                <Button type="button" variant="outline" onClick={triggerProfileImageInput}>
                  <ImageIcon className="mr-2 h-4 w-4" /> Choose Image
                </Button>
                <input
                  type="file"
                  ref={profileImageInputRef}
                  onChange={handleImageChange}
                  accept="image/*"
                  className="hidden"
                  required
                />
                {imagePreview && <img src={imagePreview} alt="Preview" className="h-16 w-16 rounded object-cover" />}
                {imageFile && <span className="text-sm text-gray-500">{imageFile.name}</span>}
              </div>
            </div>
            <Button type="submit" disabled={isAnalyzingProfile} className="w-full md:w-auto">
              {isAnalyzingProfile ? "Analyzing Profile..." : "Analyze Profile Risk"}
            </Button>
          </form>

          {/* Display Profile Analysis Results */}
          {isAnalyzingProfile && <p className="mt-4 text-center text-blue-600">Analyzing...</p>}
          {profileAnalysisResult && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mt-6 p-4 border rounded-lg bg-gray-50 dark:bg-gray-800"
            >
              <h4 className="font-semibold mb-2">Analysis Result:</h4>
              <p className="mb-2"><span className="font-medium">Description:</span> {profileAnalysisResult.description}</p>
              <p><span className="font-medium">Risk Score:</span> {getRiskScoreBadge(profileAnalysisResult.riskScore)}</p>
            </motion.div>
          )}
        </CardContent>
      </Card>

      {overallStatus !== "idle" && (
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
          {getOverallStatusAlert()}
        </motion.div>
      )}

      {(logs.length > 0 || isAnalyzing) && (
        <Card className="mb-8 border-none shadow-lg overflow-hidden">
          <CardHeader className="bg-gray-900 text-white py-3 px-4 flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-mono">Analysis Logs</CardTitle>
            <Badge className="bg-blue-600">Real-time</Badge>
          </CardHeader>
          <CardContent className="bg-gray-950 text-gray-200 p-0">
            <div className="font-mono text-sm p-4 h-[220px] overflow-y-auto">
              <AnimatePresence>
                {logs.map((log, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="mb-2"
                  >
                    <span className="text-gray-400 mr-2">{`>`}</span>
                    <span className={log.color}>{log.text}</span>
                  </motion.div>
                ))}
                {isAnalyzing && logs.length === 0 && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mb-2">
                    <span className="text-gray-400 mr-2">{`>`}</span>
                    <span className="text-blue-400">Initializing analysis...</span>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </CardContent>
        </Card>
      )}

      {transactions.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <Card className="mb-8 border-none shadow-lg overflow-hidden">
            <CardHeader className="border-b bg-white dark:bg-gray-900">
              <CardTitle>Transaction Analysis Results</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gray-50 dark:bg-gray-800 border-b">
                      <th className="text-left py-3 px-4 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        Transaction ID
                      </th>
                      <th className="text-left py-3 px-4 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        Amount
                      </th>
                      <th className="text-left py-3 px-4 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        Merchant
                      </th>
                      <th className="text-left py-3 px-4 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        Risk Score
                      </th>
                      <th className="text-left py-3 px-4 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        Status
                      </th>
                      <th className="text-left py-3 px-4 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        Forwarded To
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.map((transaction, index) => (
                      <motion.tr
                        key={transaction.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                        className={`border-b last:border-b-0 hover:bg-gray-50 dark:hover:bg-gray-800 ${
                          transaction.status === "flagged"
                            ? "bg-red-50 dark:bg-red-900/10"
                            : transaction.status === "review"
                              ? "bg-amber-50 dark:bg-amber-900/10"
                              : ""
                        }`}
                      >
                        <td className="py-3 px-4 font-medium">{transaction.id}</td>
                        <td className="py-3 px-4 font-medium">{transaction.amount}</td>
                        <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                          {transaction.merchant}
                          <div className="text-xs text-gray-500">{transaction.category}</div>
                        </td>
                        <td className="py-3 px-4">
                          {transaction.riskScore !== undefined && getRiskScoreBadge(transaction.riskScore)}
                        </td>
                        <td className="py-3 px-4">{getStatusBadge(transaction.status)}</td>
                        <td className="py-3 px-4 text-gray-600 dark:text-gray-400">{transaction.forwardedTo}</td>
                      </motion.tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          {needsAction && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Card className="border-none shadow-lg">
                <CardHeader className="border-b">
                  <CardTitle>AI Action Panel</CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <Button
                      variant="outline"
                      className="flex items-center gap-2 h-auto py-6 border-gray-300 hover:bg-blue-50 hover:border-blue-200 hover:text-blue-700 transition-colors"
                    >
                      <div className="bg-blue-100 p-2 rounded-full">
                        <MessageSquare className="h-5 w-5 text-blue-600" />
                      </div>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">Send AI Text Message</span>
                        <span className="text-xs text-gray-500">Notify customer via SMS</span>
                      </div>
                    </Button>

                    <Button
                      variant="outline"
                      className="flex items-center gap-2 h-auto py-6 border-gray-300 hover:bg-green-50 hover:border-green-200 hover:text-green-700 transition-colors"
                    >
                      <div className="bg-green-100 p-2 rounded-full">
                        <Phone className="h-5 w-5 text-green-600" />
                      </div>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">Initiate AI Phone Call</span>
                        <span className="text-xs text-gray-500">Automated verification call</span>
                      </div>
                    </Button>

                    <Button
                      variant="outline"
                      className="flex items-center gap-2 h-auto py-6 border-gray-300 hover:bg-purple-50 hover:border-purple-200 hover:text-purple-700 transition-colors"
                    >
                      <div className="bg-purple-100 p-2 rounded-full">
                        <User className="h-5 w-5 text-purple-600" />
                      </div>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">Launch AI Avatar Interview</span>
                        <span className="text-xs text-gray-500">Virtual agent verification</span>
                      </div>
                    </Button>

                    <Button
                      variant="outline"
                      className="flex items-center gap-2 h-auto py-6 border-gray-300 hover:bg-cyan-50 hover:border-cyan-200 hover:text-cyan-700 transition-colors"
                    >
                      <div className="bg-cyan-100 p-2 rounded-full">
                        <Mail className="h-5 w-5 text-cyan-600" />
                      </div>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">Send AI Email Summary</span>
                        <span className="text-xs text-gray-500">Detailed report to customer</span>
                      </div>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </motion.div>
      )}
    </main>
  )
}
