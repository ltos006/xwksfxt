// 用户角色枚举
export const USER_ROLES = {
  PATIENT: 'patient',
  DOCTOR: 'doctor',
  ADMIN: 'admin'
}

// 任务状态枚举
export const TASK_STATUS = {
  NOT_STARTED: 'not_started',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed'
}

export const TASK_STATUS_TEXT = {
  [TASK_STATUS.NOT_STARTED]: '未开始',
  [TASK_STATUS.IN_PROGRESS]: '待完成',
  [TASK_STATUS.COMPLETED]: '已完成'
}

export const TASK_STATUS_TYPE = {
  [TASK_STATUS.NOT_STARTED]: 'info',
  [TASK_STATUS.IN_PROGRESS]: 'warning',
  [TASK_STATUS.COMPLETED]: 'success'
}

// 绑定状态枚举
export const BINDING_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  UNBOUND: 'unbound'
}

export const BINDING_STATUS_TEXT = {
  [BINDING_STATUS.PENDING]: '待确认',
  [BINDING_STATUS.APPROVED]: '已绑定',
  [BINDING_STATUS.REJECTED]: '已拒绝',
  [BINDING_STATUS.UNBOUND]: '已解除'
}

export const BINDING_STATUS_TYPE = {
  [BINDING_STATUS.PENDING]: 'warning',
  [BINDING_STATUS.APPROVED]: 'success',
  [BINDING_STATUS.REJECTED]: 'danger',
  [BINDING_STATUS.UNBOUND]: 'info'
}

// 医生审核状态
export const DOCTOR_AUDIT_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected'
}

export const DOCTOR_AUDIT_STATUS_TEXT = {
  [DOCTOR_AUDIT_STATUS.PENDING]: '待审核',
  [DOCTOR_AUDIT_STATUS.APPROVED]: '已通过',
  [DOCTOR_AUDIT_STATUS.REJECTED]: '已拒绝'
}

export const DOCTOR_AUDIT_STATUS_TYPE = {
  [DOCTOR_AUDIT_STATUS.PENDING]: 'warning',
  [DOCTOR_AUDIT_STATUS.APPROVED]: 'success',
  [DOCTOR_AUDIT_STATUS.REJECTED]: 'danger'
}

// 症状分类列表（用于数值项快速选择）
export const SYMPTOM_CATEGORIES = [
  {
    name: '疼痛类',
    symptoms: ['疼痛评分', '止痛药剂量', '疼痛频率', '疼痛持续时间']
  },
  {
    name: '伤口类',
    symptoms: ['伤口愈合评分', '红肿程度', '渗液量', '换药次数']
  },
  {
    name: '生命体征',
    symptoms: ['体温', '心率', '血压(收缩压)', '血压(舒张压)', '血氧饱和度']
  },
  {
    name: '活动能力',
    symptoms: ['行走距离', '关节活动度', '日常活动评分', '运动时长']
  },
  {
    name: '用药类',
    symptoms: ['服药次数', '漏服次数', '不良反应次数', '药量(mg)']
  },
  {
    name: '饮食消化',
    symptoms: ['进食量评分', '饮水量(ml)', '排便次数', '排便形态评分']
  },
  {
    name: '睡眠心理',
    symptoms: ['睡眠时长(h)', '入睡困难评分', '焦虑评分', '抑郁评分']
  },
  {
    name: '其他',
    symptoms: ['体重(kg)', '体温(℃)', '尿量(ml)', '引流液量(ml)']
  }
]
