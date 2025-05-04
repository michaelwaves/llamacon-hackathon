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

const formSchema = z.object({
    first_name: z.string().min(1),
    last_name: z.string().min(1),
    occupation: z.string().min(1),
    image: z.any(),
})

type KYCFormValues = z.infer<typeof formSchema>

export function KYCForm() {
    const [response, setResponse] = useState<any>(null)
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<KYCFormValues>({
        resolver: zodResolver(formSchema),
    })

    const onSubmit = async (data: KYCFormValues) => {
        const formData = new FormData()
        formData.append('first_name', data.first_name)
        formData.append('last_name', data.last_name)
        formData.append('occupation', data.occupation)
        formData.append('image', data.image[0]) // file input is an array

        const res = await fetch('http://localhost:8000/kyc', {
            method: 'POST',
            body: formData,
        })

        const result = await res.json()
        setResponse(result)
    }

    return (
        <div>
            <Card className="max-w-md mx-auto mt-10 p-6 rounded-2xl shadow-xl">
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
                        <Button type="submit" className="w-full">
                            Submit KYC
                        </Button>
                    </form>
                    {response && (
                        <div className="mt-4 p-4 bg-green-100 text-green-800 rounded-md text-sm">
                            ✅ KYC submitted successfully
                        </div>
                    )}
                </CardContent>
            </Card>
            {response &&
                <>
                    <AdverseMediaPepTables pep_results={response.pep_results ?? []} adverse_media_results={response.adverse_media_results ?? []} />
                    <KYCResults data={response} />
                </>}
        </div>
    )
}
