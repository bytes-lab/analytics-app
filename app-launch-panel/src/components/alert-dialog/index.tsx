import React, { Fragment } from 'react'
import { Button, Dialog } from 'opsramp-design-system'
import { useTranslation } from 'react-i18next'
type AlertDialogProps = {
  onCancel: () => void
  onContinue: () => void
}

type AlertDialogHeaderProps = {
  onContinue: () => void
}
const AlertDialog: React.FC<AlertDialogProps> = ({
  onCancel,
  onContinue,
  children
}) => {
  const { t } = useTranslation()

  const onCancelHandler = () => {
    onCancel()
  }
  const onContinueHandler = () => {
    onContinue()
  }

  return (
    <Fragment>
      <Dialog aria-label="cancel">
        <div className="flex items-center justify-center fixed left-0 bottom-0 w-full h-full ">
          <div className="bg-white rounded-lg ops-trigger-container max-w-md">
            <div className="flex flex-col items-start">
              <div className="body-2 p-5 pr-10">{children}</div>
              <div className="ml-auto pr-5 pb-5">
                <Button
                  type="button"
                  onClick={onCancelHandler}
                  className="mr-5 ops-text-grey-800"
                  variant="text"
                >
                  {t('close-alert.cancel')}
                </Button>
                <Button variant="text" onClick={onContinueHandler}>
                  {t('close-alert.continue')}
                </Button>
              </div>
            </div>
            <button
              tabIndex={0}
              className="ops-trigger-close ops-text-grey-800 block"
              onClick={onCancelHandler}
            >
              <i className="icon-close" aria-label="close"></i>
            </button>
          </div>
        </div>
      </Dialog>
    </Fragment>
  )
}

const AlertDialogHeader: React.FC<AlertDialogHeaderProps> = ({
  onContinue,
  children
}) => {
  const { t } = useTranslation()

  const onContinueHandler = () => {
    onContinue()
  }

  return (
    <Fragment>
      <Dialog aria-label="cancel">
        <div className="flex items-center justify-center fixed left-0 bottom-0 w-full h-full ">
          <div className="bg-white rounded-lg ops-trigger-container max-w-md">
            <div>
              <span
                className="flex flex-row font-semibold mt-3	 text-gray-700 text-lg font-sans ml-8
"
              >
                {t('access_denied.header')}
              </span>
            </div>
            <div className="flex flex-col items-start">
              <div className="body-2 p-3 mt-2 pl-8 pr-5">{children}</div>
              <div className="ml-auto pr-5 mt-2  pb-5 ">
                <Button
                  variant="text"
                  className="outline-none focus:outline-none !important"
                  onClick={onContinueHandler}
                >
                  {t('ok')}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Dialog>
    </Fragment>
  )
}
export { AlertDialog, AlertDialogHeader }
