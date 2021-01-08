import React, { useState, useEffect } from 'react'
import { Checkbox } from 'opsramp-design-system'

type ActionItemBooleanProps = {
  action: { name: string; label: string }
  onChange: ({
    actionName,
    actionType,
    isChecked
  }: {
    actionName: string
    actionType: 'text' | 'boolean'
    isChecked: boolean
  }) => void
}

function ActionItemBoolean({ action, onChange }: ActionItemBooleanProps) {
  const [isChecked, setIsChecked] = useState(false)

  useEffect(() => {
    onChange({ actionName: action.name, isChecked, actionType: 'boolean' })
  }, [action.name, isChecked, onChange])

  return (
    <Checkbox
      className="body-1 ops-text-grey-800 whitespace-no-wrap"
      value={action.name}
      onChange={setIsChecked}
    >
      {action.label}
    </Checkbox>
  )
}

export default ActionItemBoolean
