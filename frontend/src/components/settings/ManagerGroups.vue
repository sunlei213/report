<template>
  <div class="manager-groups">
    <!-- 组列表 -->
    <div class="group-list">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>客户经理组</span>
            <el-button type="primary" @click="addGroup">添加组</el-button>
          </div>
        </template>
        
        <el-table :data="groups" border>
          <el-table-column label="组名" prop="name" />
          <el-table-column label="排序" width="100">
            <template #default="{ row, $index }">
              <el-button-group>
                <el-button 
                  :disabled="$index === 0"
                  @click="moveGroup($index, -1)"
                  icon="el-icon-top"
                  size="small"
                />
                <el-button 
                  :disabled="$index === groups.length - 1"
                  @click="moveGroup($index, 1)"
                  icon="el-icon-bottom"
                  size="small"
                />
              </el-button-group>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                size="small"
                @click="editGroup(row)"
              >
                编辑
              </el-button>
              <el-button 
                type="danger" 
                size="small"
                @click="deleteGroup(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 组成员管理 -->
    <div class="group-members" v-if="selectedGroup">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>{{ selectedGroup.name }} - 成员管理</span>
            <el-button type="primary" @click="addManager">添加成员</el-button>
          </div>
        </template>
        
        <el-table :data="managers" border>
          <el-table-column label="姓名" prop="name" />
          <el-table-column label="指标" prop="target">
            <template #default="{ row }">
              <el-input-number 
                v-model="row.target" 
                :min="0"
                @change="updateManager(row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="排序" width="100">
            <template #default="{ row, $index }">
              <el-button-group>
                <el-button 
                  :disabled="$index === 0"
                  @click="moveManager($index, -1)"
                  icon="el-icon-top"
                  size="small"
                />
                <el-button 
                  :disabled="$index === managers.length - 1"
                  @click="moveManager($index, 1)"
                  icon="el-icon-bottom"
                  size="small"
                />
              </el-button-group>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button 
                type="danger" 
                size="small"
                @click="deleteManager(row)"
              >
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 组对话框 -->
    <el-dialog
      :title="groupDialog.title"
      v-model="groupDialog.visible"
      width="500px"
    >
      <el-form :model="groupDialog.form" label-width="80px">
        <el-form-item label="组名">
          <el-input v-model="groupDialog.form.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="groupDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveGroup">确定</el-button>
      </template>
    </el-dialog>

    <!-- 成员对话框 -->
    <el-dialog
      title="添加成员"
      v-model="managerDialog.visible"
      width="500px"
    >
      <el-form :model="managerDialog.form" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="managerDialog.form.name" />
        </el-form-item>
        <el-form-item label="指标">
          <el-input-number 
            v-model="managerDialog.form.target"
            :min="0"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="managerDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveManager">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ManagerGroups',
  data() {
    return {
      groups: [],
      managers: [],
      selectedGroup: null,
      groupDialog: {
        visible: false,
        title: '',
        form: {
          name: '',
          id: null
        }
      },
      managerDialog: {
        visible: false,
        form: {
          name: '',
          target: 0
        }
      }
    }
  },
  created() {
    this.fetchGroups()
  },
  methods: {
    async fetchGroups() {
      try {
        const res = await axios.get('/api/settings/manager-groups')
        this.groups = res.data
      } catch (error) {
        this.$message.error('获取组列表失败')
      }
    },
    async fetchManagers() {
      if (!this.selectedGroup) return
      try {
        const res = await axios.get(`/api/settings/manager-groups/${this.selectedGroup.id}/managers`)
        this.managers = res.data
      } catch (error) {
        this.$message.error('获取成员列表失败')
      }
    },
    addGroup() {
      this.groupDialog.title = '添加组'
      this.groupDialog.form = { name: '', id: null }
      this.groupDialog.visible = true
    },
    editGroup(group) {
      this.groupDialog.title = '编辑组'
      this.groupDialog.form = { ...group }
      this.groupDialog.visible = true
    },
    async saveGroup() {
      try {
        if (this.groupDialog.form.id) {
          await axios.put(`/api/settings/manager-groups/${this.groupDialog.form.id}`, this.groupDialog.form)
        } else {
          await axios.post('/api/settings/manager-groups', this.groupDialog.form)
        }
        this.groupDialog.visible = false
        this.fetchGroups()
        this.$message.success('保存成功')
      } catch (error) {
        this.$message.error('保存失败')
      }
    },
    async deleteGroup(group) {
      try {
        await this.$confirm('确认删除该组?', '提示', {
          type: 'warning'
        })
        await axios.delete(`/api/settings/manager-groups/${group.id}`)
        this.fetchGroups()
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    },
    async moveGroup(index, direction) {
      const newIndex = index + direction
      try {
        await axios.put('/api/settings/manager-groups/reorder', {
          id: this.groups[index].id,
          newOrder: this.groups[newIndex].order
        })
        this.fetchGroups()
      } catch (error) {
        this.$message.error('移动失败')
      }
    },
    addManager() {
      this.managerDialog.form = { name: '', target: 0 }
      this.managerDialog.visible = true
    },
    async saveManager() {
      try {
        await axios.post(`/api/settings/manager-groups/${this.selectedGroup.id}/managers`, 
          this.managerDialog.form)
        this.managerDialog.visible = false
        this.fetchManagers()
        this.$message.success('添加成功')
      } catch (error) {
        this.$message.error('添加失败')
      }
    },
    async updateManager(manager) {
      try {
        await axios.put(`/api/settings/managers/${manager.id}`, manager)
        this.$message.success('更新成功')
      } catch (error) {
        this.$message.error('更新失败')
      }
    },
    async deleteManager(manager) {
      try {
        await this.$confirm('确认移除该成员?', '提示', {
          type: 'warning'
        })
        await axios.delete(`/api/settings/managers/${manager.id}`)
        this.fetchManagers()
        this.$message.success('移除成功')
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('移除失败')
        }
      }
    },
    async moveManager(index, direction) {
      const newIndex = index + direction
      try {
        await axios.put('/api/settings/managers/reorder', {
          id: this.managers[index].id,
          newOrder: this.managers[newIndex].order
        })
        this.fetchManagers()
      } catch (error) {
        this.$message.error('移动失败')
      }
    }
  }
}
</script>

<style scoped>
.manager-groups {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 