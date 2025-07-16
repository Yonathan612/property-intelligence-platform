"use client";

import Link from "next/link";
import { Button } from "../button";
import { H3 } from "../typography";
import { usePathname } from "next/navigation";
import { Kanit } from "next/font/google";
import { cn } from "@/lib/utils";

const kanit = Kanit({
  weight: ["100", "200", "300", "400", "500", "600", "700", "800"],
  subsets: ["latin"],
});

type NavOption = {
  name: string;
  href: string;
};
const navOptions: NavOption[] = [
  {
    name: "Property Search",
    href: "/property-search",
  },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <div className="w-full h-16 flex justify-between items-center px-6 border-b border-border bg-white">
      <Link href={"/"} className={"flex items-center gap-2"}>
        <H3 className={`font-medium text-2xl ${kanit.className}`}>
          Property Search Tool
        </H3>
      </Link>

      <div className={"flex gap-8 items-center"}>
        {navOptions.map((navOption, index) => (
          <Link
            href={navOption.href}
            className={cn(
              "text-neutral-500 text-sm font-semibold underline-offset-[8px] decoration-neutral-300 hover:underline hover:decoration-2 hover:text-black transition-all",
              pathname === navOption.href ? "text-black underline" : ""
            )}
            key={index}
          >
            {navOption.name}
          </Link>
        ))}
      </div>
    </div>
  );
}
