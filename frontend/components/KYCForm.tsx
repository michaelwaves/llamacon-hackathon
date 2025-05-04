'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import KYCResults from './KYCResults'
import { AdverseMediaPepTables } from './AdverseMediaPepTables'
import Image from 'next/image'
import { Loader } from 'lucide-react'

const formSchema = z.object({
    first_name: z.string().min(1),
    last_name: z.string().min(1),
    occupation: z.string().min(1),
    image: z.any(),
})

type KYCFormValues = z.infer<typeof formSchema>

export function KYCForm() {
    const [response, setResponse] = useState<any>(null)
    const [previewUrl, setPreviewUrl] = useState<string | null>(null)
    const [isSubmitting, setIsSubmitting] = useState(false)
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<KYCFormValues>({
        resolver: zodResolver(formSchema),
    })

    const onSubmit = async (data: KYCFormValues) => {
        setIsSubmitting(true)
        const formData = new FormData()
        formData.append('first_name', data.first_name)
        formData.append('last_name', data.last_name)
        formData.append('occupation', data.occupation)
        formData.append('image', data.image[0]) // file input is an array

        // preview image
        const imageUrl = URL.createObjectURL(data.image[0])
        setPreviewUrl(imageUrl)

        const res = await fetch('http://localhost:8000/kyc', {
            method: 'POST',
            body: formData,
        })

        const result = await res.json()
        setResponse(result)
        setIsSubmitting(false)
    }

    return (
        <div className='p-6'>
            <div className='flex flex-row items-center justify-center gap-6'>
                <div className='flex flex-row gap-4'>
                    <Card className="max-w-md mx-auto w-full mt-10 p-6 rounded-2xl shadow-xl">
                        <CardContent>
                            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                                <div>
                                    <Label htmlFor="first_name">First Name</Label>
                                    <Input id="first_name" {...register('first_name')} />
                                    {errors.first_name && (
                                        <p className="text-red-500 text-sm">{errors.first_name.message}</p>
                                    )}
                                </div>
                                <div>
                                    <Label htmlFor="last_name">Last Name</Label>
                                    <Input id="last_name" {...register('last_name')} />
                                    {errors.last_name && (
                                        <p className="text-red-500 text-sm">{errors.last_name.message}</p>
                                    )}
                                </div>
                                <div>
                                    <Label htmlFor="occupation">Occupation</Label>
                                    <Input id="occupation" {...register('occupation')} />
                                    {errors.occupation && (
                                        <p className="text-red-500 text-sm">{errors.occupation.message}</p>
                                    )}
                                </div>
                                <div>
                                    <Label htmlFor="image">Upload Image</Label>
                                    <Input id="image" type="file" accept="image/*" {...register('image')} />
                                    {errors.image && (
                                        <p className="text-red-500 text-sm">{errors.image.message as String}</p>
                                    )}
                                </div>
                                <Button type="submit" className="w-full" disabled={isSubmitting}>
                                    {isSubmitting ? <Loader className='animate-spin' /> : "Submit KYC"}
                                </Button>
                            </form>
                            {response && (
                                <div className="mt-4 p-4 bg-green-100 text-green-800 rounded-md text-sm">
                                    ✅ KYC submitted successfully
                                </div>
                            )}
                        </CardContent>
                    </Card>
                    {previewUrl && (
                        <div className="flex justify-center items-center border rounded-lg p-4 bg-gray-50">
                            <Image
                                src={previewUrl}
                                alt="Uploaded preview"
                                className="max-h-96 object-contain rounded-md shadow-md"
                                width={1000}
                                height={1000}
                            />
                        </div>
                    )}
                </div>
                {response && <KYCResults data={response} />}
            </div>
            {response &&
                <>
                    <AdverseMediaPepTables
                        pep_results={response.pep_results ?? []}
                        adverse_media_results={response.adverse_media_results ?? []}
                        court_results={response.court_cases_results ?? []}
                    />
                </>}
        </div>
    )
}
