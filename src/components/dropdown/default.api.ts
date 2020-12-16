export type DefaultDropdownProps = {
  disabled?: boolean
  data: string[]
  defaultToggleLabel: string
  initialValue?: string | null
  placeholder?: string
  hideSearch?: boolean
  onChange: (value?: string | null) => void
}
