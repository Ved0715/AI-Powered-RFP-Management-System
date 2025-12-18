"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Loader2, Pencil } from "lucide-react";

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

interface Vendor {
  id: string;
  name: string;
  email: string;
  contact_person: string;
  phone?: string;
  notes?: string;
}

interface EditVendorSheetProps {
  vendor: Vendor;
  onVendorUpdated: (vendor: Vendor) => void;
}

export function EditVendorSheet({
  vendor,
  onVendorUpdated,
}: EditVendorSheetProps) {
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
      name: vendor.name,
      contact_person: vendor.contact_person,
      email: vendor.email,
      phone: vendor.phone || "",
      notes: vendor.notes || "",
    },
  });

  useEffect(() => {
    if (open) {
      reset({
        name: vendor.name,
        contact_person: vendor.contact_person,
        email: vendor.email,
        phone: vendor.phone || "",
        notes: vendor.notes || "",
      });
    }
  }, [open, vendor, reset]);

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    setIsLoading(true);
    try {
      const res = await fetch(
        `http://localhost:8000/api/vendors/${vendor.id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(values),
        }
      );

      if (res.ok) {
        const updatedVendor = await res.json();
        onVendorUpdated(updatedVendor);
        setOpen(false);
      } else {
        alert("Failed to update vendor");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <button
          className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
          title="Edit Vendor"
        >
          <Pencil className="h-4 w-4" />
        </button>
      </SheetTrigger>
      <SheetContent className="sm:max-w-[600px] p-4">
        <SheetHeader>
          <SheetTitle>Edit Vendor</SheetTitle>
          <SheetDescription>
            Update the details for {vendor.name}. Click save when you're done.
          </SheetDescription>
        </SheetHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-4">
          <div className="space-y-2">
            <Label htmlFor="edit-name">Company Name</Label>
            <Input
              id="edit-name"
              placeholder="Acme Corp"
              {...register("name")}
            />
            {errors.name && (
              <p className="text-sm text-red-500">{errors.name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="edit-contact_person">Contact Person</Label>
            <Input
              id="edit-contact_person"
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
            <Label htmlFor="edit-email">Email</Label>
            <Input
              id="edit-email"
              type="email"
              placeholder="contact@acme.com"
              {...register("email")}
            />
            {errors.email && (
              <p className="text-sm text-red-500">{errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="edit-phone">Phone (Optional)</Label>
            <Input
              id="edit-phone"
              placeholder="+1 234 567 890"
              {...register("phone")}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="edit-notes">Note (Optional)</Label>
            <Input
              id="edit-notes"
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
                  Updating...
                </>
              ) : (
                "Save Changes"
              )}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}
