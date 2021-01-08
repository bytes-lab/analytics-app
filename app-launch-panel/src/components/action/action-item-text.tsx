import React, { useState, useEffect } from 'react'
import { useFormik } from 'formik'
import * as Yup from 'yup'
import { noop } from '@reach/utils'
import { Checkbox, TextInput } from 'opsramp-design-system'
import ErrorMessage from 'components/error-message'

type ActionItemTextProps = {
  action: { name: string; label: string }
  defaultValue?: string
  placeholder?: string
  onChange: ({
    actionName,
    actionValue,
    actionType,
    isChecked
  }: {
    actionName: string
    actionValue?: string
    actionType: 'text' | 'boolean'
    isChecked: boolean
  }) => void
}

function ActionItemText({
  action,
  defaultValue = '',
  placeholder,
  onChange
}: ActionItemTextProps) {
  const [isChecked, setIsChecked] = useState(false)

  const {
    errors,
    touched,
    handleBlur,
    setFieldValue,
    isValid,
    values,
    ...formik
  } = useFormik({
    initialValues: { [action.name]: '' },
    validationSchema: Yup.object().shape({
      [action.name]: Yup.string().required(`${action.label} is required`)
    }),
    onSubmit: noop,
    validateOnMount: true
  })

  function handleChange(
    _: string,
    event?: React.ChangeEvent<HTMLInputElement>
  ) {
    formik.handleChange(event!)
  }

  useEffect(() => {
    onChange({
      actionName: action.name,
      isChecked,
      actionValue: values[action.name],
      actionType: 'text'
    })
  }, [action.name, isChecked, isValid, onChange, values])

  return (
    <>
      <div>
        <Checkbox
          className="body-1 ops-text-grey-800 whitespace-no-wrap"
          value={action.name}
          onChange={setIsChecked}
        >
          {action.label}
        </Checkbox>
      </div>

      {isChecked ? (
        <div>
          <TextInput
            value={values[action.name]}
            name={action.name}
            placeholder={placeholder}
            onChange={handleChange}
            onBlur={handleBlur}
            autoFocus
          />
          <ErrorMessage
            show={!!(touched[action.name] && errors[action.name])}
          >{`${action.label} is required`}</ErrorMessage>
        </div>
      ) : (
        <div></div>
      )}
    </>
  )
}

export default ActionItemText
