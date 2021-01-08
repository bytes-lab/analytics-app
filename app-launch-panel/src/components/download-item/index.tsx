import React from 'react'
import { Button } from 'opsramp-design-system'
import { useTranslation } from 'react-i18next'
import clsx from 'clsx'

export type DownloadItemProps = {
  image: string
  label: string
  link: string
  version?: string
  arch?: string
}

function DownloadItem({
  image,
  label,
  link,
  version,
  arch
}: DownloadItemProps) {
  const { t } = useTranslation()
  return (
    <div className="border rounded inline-block text-center w-auto mt-5 p-5">
      <div className={clsx(image, 'mx-auto transform scale-80')} />
      <div className="py-5 body-1 font-bold">{label}</div>
      <div>{version}</div>
      <a href={link} download>
        <Button className="uppercase" type="button" variant="secondary">
          {t('download')}
        </Button>
      </a>
      <div className="pt-2 body-3 font-bold">{arch}</div>
    </div>
  )
}

export default DownloadItem
