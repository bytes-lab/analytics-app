export type DrowdownProps<T> = {
  /**
   * Toggle button will be disaled when this prop has value true
   */
  disabled?: boolean

  /**
   * List of all items of the dropdown
   */
  items: T[]

  /**
   * Pass an item that should be selected when dropdown is initialized.
   */
  initialValue?: T | null

  /**
   * Pass an item that should be selected when dropdown is reset
   */
  defaultValue?: T | null

  /**
   * Search input's placeholder
   */
  placeholder?: string

  /**
   * Toggle button label. By default it will display the string value of current
   * item. The string value will get from itemToString props
   */
  toggleButtonLabel?: React.ReactNode

  /**
   * Show when filtering returns no item
   */
  noFilterResultLabel?: React.ReactNode

  /**
   * Hide search box
   */
  hideSearch?: boolean

  containerClasses?: string

  toggleButtonClasses?: string

  popoverClasses?: string

  inputClasses?: string

  menuClasses?: string

  /**
   * If your items are stored as an objects instead on a strings, Dropdown still
   * needs a string representation for each one.
   *
   * Note: This callback must include a null check: it is invoked with null
   * whenever the user abandons input via <ESC>
   *
   * @default
   *
   * // Item is a string
   * function itemToString(item?: string) {
   *   return (item ? String(item) : '')
   * }
   *
   * @example
   *
   * // Item is an object: {id: string, name: string}
   * function itemToString(item?: {id: string, name: string}) {
   *   return (item ? item.name : '')
   * }
   */
  itemToString?: (item?: T | null) => string

  /**
   * Call each time the selected item was changed. Selection can be performed by
   * item click, Enter key while item is highlighted or by blurring the menu
   * while an item is highlighted (Tab, Shift-Tab or clicking away).
   */
  onChange?: (selectedItem?: T | null) => void

  /**
   * Filter callback when the value of search input change.
   *
   * @return filtered items
   *
   * @example
   *
   * function Component() {
   *   const items: ['hello', 'to', 'the', 'new', 'word']
   *
   *   function handleInputValueChange(items: string[], searchQuery: string) {
   *     return items.filter(item => item.starstWith(searchQuery))
   *   }
   *
   *   return (
   *     <Dropdown
   *       filterHandler={handleFilterInSearch}
   *       { ...otherProps }
   *     />
   *   )
   * }
   */
  filterHandler: (defaultData: T[], searchQuery?: string) => T[]
}
