export function clsx(...values: ClassValue[]): string {
  return values.filter(Boolean).join(' ')
}

type ClassValue = string | false | null | undefined
