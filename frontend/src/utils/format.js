export const CURRENCY = 'Đ'

export const toNumber = (value) => {
  if (value === null || value === undefined || value === '') return null
  const n = Number(value)
  return Number.isFinite(n) ? n : null
}

export const formatMoney = (value, decimals = 2) => {
  const n = toNumber(value)
  if (n === null) return `${CURRENCY} —`
  return `${CURRENCY} ${n.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })}`
}

export const formatSignedMoney = (value, decimals = 2) => {
  const n = toNumber(value)
  if (n === null) return `${CURRENCY} —`
  const sign = n > 0 ? '+' : ''
  const amount = Math.abs(n).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
  return `${CURRENCY} ${sign}${amount}`
}

export const formatDate = (value, options = { day: 'numeric', month: 'short' }) => {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleDateString('en-US', options)
}

export const formatMonth = (value) => {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}
