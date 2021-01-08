/**
 * Default MultiSelect is used items which have type string
 *
 */
export type DefaultMultiSelectProps = {
  /**
   * Toggle button will be disaled when this prop has value true
   */
  disabled?: boolean

  /**
   * Show the select all / deselect all item when this prop has value true
   */
  selectAll?: boolean

  /**
   * List of all items of the dropdown
   */
  data: string[]

  /**
   * Toggle button label. By default it will display the string value of current
   * item. The string value will get from itemToString props
   */
  defaultToggleLabel: string

  /**
   * Pass an item that should be selected when dropdown is initialized.
   */
  initialValues?: string[]

  /**
   * Pass an item that should be selected when dropdown is reset
   */
  defaultValues?: string[]

  /**
   * Search input's placeholder
   */
  placeholder?: string

  /**
   * Show when filtering returns no item
   */
  noFilterResultLabel?: React.ReactNode

  /**
   * Call each time the selected item was changed. Selection can be performed by
   * item click, Enter key while item is highlighted or by blurring the menu
   * while an item is highlighted (Tab, Shift-Tab or clicking away).
   */
  onChange?: (selectedItems?: string[] | null) => void
}

/*
 * For example:
 *
const items = [
  'Neptunium',
  'Plutonium',
  'Americium',
  'Curium',
  'Berkelium',
  'Californium',
  'Einsteinium',
  'Fermium',
  'Mendelevium',
  'Nobelium',
  'Lawrencium',
  'Rutherfordium',
  'Dubnium',
  'Seaborgium',
  'Bohrium',
  'Hassium',
  'Meitnerium',
  'Darmstadtium',
  'Roentgenium',
  'Copernicium',
  'Nihonium',
  'Flerovium',
  'Moscovium',
  'Livermorium',
  'Tennessine',
  'Oganesson'
]

const Test: React.FC = () => {
  return (
    <div style={{ width: 300 }} className="mx-auto py-16">
      <MultiSelect
        data={items}
        defaultToggleLabel="default toggle"
      />
    </div>
  )
}


*/
