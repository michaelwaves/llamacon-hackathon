'use client'

import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Card } from '@/components/ui/card'
import Link from 'next/link'

type ResultItem = {
    title: string
    text: string
    href: string
}

type Props = {
    pep_results: ResultItem[]
    adverse_media_results: ResultItem[]
    court_results: ResultItem[]
}

export function AdverseMediaPepTables({ pep_results, adverse_media_results, court_results }: Props) {
    const renderTable = (items: ResultItem[]) => (
        <div className="overflow-auto">
            <table className="w-full table-auto border mt-2">
                <thead className="bg-gray-100 text-left">
                    <tr>
                        <th className="px-4 py-2">Title</th>
                        <th className="px-4 py-2">Text</th>
                        <th className="px-4 py-2">Link</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map((item, idx) => (
                        <tr key={idx} className="border-t">
                            <td className="px-4 py-2">{item.title}</td>
                            <td className="px-4 py-2 text-sm">{item.text}</td>
                            <td className="px-4 py-2">
                                <Link
                                    href={item.href}
                                    className="text-green-700 underline"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    View Source
                                </Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )

    return (
        <Card className="mt-6 p-4">
            <Tabs defaultValue="pep" className="w-full">
                <TabsList>
                    <TabsTrigger value="pep">PEP Results</TabsTrigger>
                    <TabsTrigger value="adverse">Adverse Media</TabsTrigger>
                    <TabsTrigger value="court">Court Cases</TabsTrigger>

                </TabsList>

                <TabsContent value="pep">{renderTable(pep_results)}</TabsContent>
                <TabsContent value="adverse">{renderTable(adverse_media_results)}</TabsContent>
                <TabsContent value="court">{renderTable(court_results)}</TabsContent>

            </Tabs>
        </Card>
    )
}
