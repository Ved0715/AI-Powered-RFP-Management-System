"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Loader2, Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
  SheetFooter,
  SheetClose,
} from "@/components/ui/sheet";

const formSchema = z.object({
  name: z.string().min(2, "Company name must be at least 2 characters"),
  contact_person: z.string().min(2, "Contact person is required"),
  email: z.string().email("Invalid email address"),
  phone: z.string().optional(),
  notes: z.string().optional(),
});

interface AddVendorSheetProps {
  onVendorAdded: (vendor: any) => void;
}

export function AddVendorSheet({ onVendorAdded }: AddVendorSheetProps) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      contact_person: "",
      email: "",
      phone: "",
      notes: "",
    },
  });

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/vendors/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      if (res.ok) {
        const newVendor = await res.json();
        onVendorAdded(newVendor);
        setOpen(false);
        reset();
      } else {
        alert("Failed to create vendor");
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Plus className="mr-2 h-4" />
          Add Vendor
        </Button>
      </SheetTrigger>
      <SheetContent className="sm:max-w-[600px] p-4">
        <SheetHeader>
          <SheetTitle>Add New Vendor</SheetTitle>
          <SheetDescription>
            Enter the details of your new supplier here. Click save when you're
            done.
          </SheetDescription>
        </SheetHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-4">
          <div className="space-y-2">
            <Label htmlFor="name">Company Name</Label>
            <Input id="name" placeholder="Acme Corp" {...register("name")} />
            {errors.name && (
              <p className="text-sm text-red-500">{errors.name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="contact_person">Contact Person</Label>
            <Input
              id="contact_person"
              placeholder="John Doe"
              {...register("contact_person")}
            />
            {errors.contact_person && (
              <p className="text-sm text-red-500">
                {errors.contact_person.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="contact@acme.com"
              {...register("email")}
            />
            {errors.email && (
              <p className="text-sm text-red-500">{errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">Phone (Optional)</Label>
            <Input
              id="phone"
              placeholder="+1 234 567 890"
              {...register("phone")}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="notes">Note (Optional)</Label>
            <Input
              id="notes"
              placeholder="Write a short note about the vendor"
              {...register("notes")}
            />
          </div>

          <SheetFooter className="">
            <SheetClose asChild>
              <Button variant="outline" type="button">
                Cancel
              </Button>
            </SheetClose>
            <Button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating...
                </>
              ) : (
                "Create Vendor"
              )}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}
