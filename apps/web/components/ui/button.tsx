import { ButtonHTMLAttributes } from "react";
import clsx from "clsx";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost";
};

export function Button({ className, variant = "primary", ...props }: Props) {
  return (
    <button
      className={clsx(
        "rounded-md px-3 py-2 text-sm font-medium transition",
        variant === "primary"
          ? "bg-[#f4a259] text-slate-900 hover:bg-[#ffc48b]"
          : "border border-slate-400/40 text-slate-100 hover:border-slate-200/70",
        className
      )}
      {...props}
    />
  );
}
